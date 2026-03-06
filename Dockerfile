FROM python:3.12-slim

# System dependencies for faster-whisper (audio decoding)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install Python dependencies (cached layer)
COPY pyproject.toml .
RUN uv sync --no-dev --no-install-project

# Copy application code
COPY app/ app/

# Pre-download the default Whisper model
RUN uv run python -c "from faster_whisper import WhisperModel; WhisperModel('small', device='cpu', compute_type='int8')"

ENTRYPOINT ["uv", "run", "python", "-m", "app.main"]
