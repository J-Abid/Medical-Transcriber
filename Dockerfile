# =============================================================================
# Dockerfile — Medical Transcriber
# =============================================================================
# Builds a lightweight container that runs the Streamlit application.
#
# Build:  docker build -t medical-transcriber .
# Run:    docker run -p 8501:8501 medical-transcriber
#
# Workflow:
#   1. Start from a slim Python base image.
#   2. Install system dependencies (ffmpeg for audio processing).
#   3. Install uv (fast Python package manager).
#   4. Copy project files into the container.
#   5. Install Python dependencies with uv.
#   6. Expose Streamlit's default port (8501).
#   7. Set the entrypoint to launch Streamlit.
# =============================================================================

# --- Step 1: Base image ---
FROM python:3.12-slim AS base

# --- Step 2: System dependencies ---
# ffmpeg is required by faster-whisper to decode audio files (WAV, MP3, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# --- Step 3: Install uv ---
# uv is a blazing-fast Python package manager written in Rust.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# --- Step 4: Copy project files ---
WORKDIR /app
COPY pyproject.toml .
COPY config.py .
COPY audio_processor.py .
COPY llm_extractor.py .
COPY app.py .

# --- Step 5: Install Python dependencies ---
# We use uv pip install to read from pyproject.toml
RUN uv pip install --system -e .

# --- Step 6: Expose Streamlit port ---
EXPOSE 8501

# --- Step 7: Health-check and entrypoint ---
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Streamlit configuration:
#   --server.headless=true       → no browser auto-open
#   --server.address=0.0.0.0     → listen on all interfaces
#   --server.port=8501           → default Streamlit port
#   --browser.gatherUsageStats=false → disable telemetry
ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.headless=true", \
    "--server.address=0.0.0.0", \
    "--server.port=8501", \
    "--browser.gatherUsageStats=false"]
