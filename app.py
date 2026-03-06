"""
app.py — Main Streamlit UI Entry Point
=======================================
This is the front-end of the Medical Transcriber application.

Workflow:
  1. User uploads a WAV or MP3 audio file via the Streamlit file uploader.
  2. The audio file is saved to a temporary location on disk.
  3. The audio is transcribed to German text using Whisper (audio_processor).
  4. The transcription is sent to an LLM to extract structured clinical data (llm_extractor).
  5. Both the transcription and the structured JSON are displayed in the UI.

UI Theme: Dark mode with Orange (#FF6B00) and Black color scheme.
"""

import os
import json
import tempfile

import streamlit as st

import config
from audio_processor import transcribe_audio
from llm_extractor import extract_clinical_data


# ---------------------------------------------------------------------------
# Page Configuration & Custom Dark Theme (Orange + Black)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="🩺 Medical Transcriber",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Inject custom CSS for a sleek dark-orange theme
st.markdown(
    """
    <style>
    /* ---- Global dark background ---- */
    .stApp {
        background-color: #0D0D0D;
        color: #E0E0E0;
    }

    /* ---- Header / Title styling ---- */
    h1, h2, h3, h4 {
        color: #FF6B00 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* ---- Sidebar dark ---- */
    section[data-testid="stSidebar"] {
        background-color: #1A1A1A;
    }

    /* ---- File uploader border glow ---- */
    section[data-testid="stFileUploader"] {
        border: 2px dashed #FF6B00;
        border-radius: 12px;
        padding: 1rem;
        background-color: #1A1A1A;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        background-color: #FF6B00 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background-color: #FF8C33 !important;
        box-shadow: 0 0 15px rgba(255, 107, 0, 0.5) !important;
    }

    /* ---- Spinner text ---- */
    .stSpinner > div > div {
        color: #FF6B00 !important;
    }

    /* ---- JSON / code blocks ---- */
    pre {
        background-color: #1A1A1A !important;
        border: 1px solid #FF6B00 !important;
        border-radius: 8px !important;
        color: #E0E0E0 !important;
    }

    /* ---- Success / info / warning boxes ---- */
    .stAlert {
        background-color: #1A1A1A !important;
        border-left-color: #FF6B00 !important;
    }

    /* ---- Divider ---- */
    hr {
        border-color: #FF6B00 !important;
    }

    /* ---- Expander header ---- */
    details > summary {
        color: #FF6B00 !important;
        font-weight: 600;
    }

    /* ---- Metric cards ---- */
    [data-testid="stMetric"] {
        background-color: #1A1A1A;
        border: 1px solid #FF6B00;
        border-radius: 10px;
        padding: 1rem;
    }
    [data-testid="stMetricLabel"] {
        color: #FF6B00 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# UI Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; padding: 1rem 0 0.5rem 0;">
        <h1 style="font-size:2.5rem; margin-bottom:0;">🩺 Medical Transcriber</h1>
        <p style="color:#999; font-size:1.1rem; margin-top:0.3rem;">
            German Medical Dictation → Structured Clinical Data
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()


# ---------------------------------------------------------------------------
# Sidebar — Configuration Display
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown(f"**Whisper Model:** `{config.WHISPER_MODEL_SIZE}`")
    st.markdown(f"**Device:** `{config.WHISPER_DEVICE}`")
    st.markdown(f"**Compute Type:** `{config.WHISPER_COMPUTE_TYPE}`")
    st.divider()
    st.markdown(f"**LLM Base URL:** `{config.LLM_BASE_URL}`")
    st.markdown(f"**LLM Model:** `{config.LLM_MODEL_NAME}`")
    st.markdown(f"**Temperature:** `{config.LLM_TEMPERATURE}`")


# ---------------------------------------------------------------------------
# Step 1: File Upload
# ---------------------------------------------------------------------------
st.markdown("### 📁 Upload Audio File")
uploaded_file = st.file_uploader(
    "Drag and drop a WAV or MP3 file with a German medical dictation.",
    type=config.ALLOWED_EXTENSIONS,
    help="Supported formats: WAV, MP3",
)


# ---------------------------------------------------------------------------
# Steps 2–5: Process when a file is uploaded
# ---------------------------------------------------------------------------
if uploaded_file is not None:
    # Show a small audio player so the user can listen to what they uploaded
    st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")

    # --- Step 2: Save the uploaded file to a temp location ---
    # We need a file path on disk because faster-whisper reads from file paths.
    os.makedirs(config.TEMP_AUDIO_DIR, exist_ok=True)
    temp_path = os.path.join(config.TEMP_AUDIO_DIR, uploaded_file.name)

    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.markdown("---")

    # --- Step 3: Transcribe with Whisper ---
    st.markdown("### 🎙️ Transcription")
    with st.spinner("Transcribing audio with Whisper… ⏳"):
        try:
            transcription = transcribe_audio(temp_path)
        except Exception as exc:
            st.error(f"❌ Transcription failed: {exc}")
            st.stop()

    # Display the raw transcription in an expandable box
    with st.expander("📝 Raw Transcription (German)", expanded=True):
        st.write(transcription)

    st.markdown("---")

    # --- Step 4: Extract structured clinical data via LLM ---
    st.markdown("### 🧠 Clinical Data Extraction")
    with st.spinner("Extracting clinical data with LLM… ⏳"):
        try:
            clinical_data = extract_clinical_data(transcription)
        except Exception as exc:
            st.error(f"❌ LLM extraction failed: {exc}")
            st.stop()

    # --- Step 5: Display the structured JSON output ---
    # Show each field as a styled card
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Beschwerde (Complaint)", value="—")
        st.info(clinical_data.get("patient_complaint", "—"))
    with col2:
        st.metric(label="Diagnose (Diagnosis)", value="—")
        st.info(clinical_data.get("diagnosis", "—"))

    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="Befunde (Findings)", value="—")
        st.info(clinical_data.get("findings", "—"))
    with col4:
        st.metric(label="Nächste Schritte (Next Steps)", value="—")
        st.info(clinical_data.get("next_steps", "—"))

    # Also show the full JSON in a code block
    with st.expander("🔍 Full JSON Output", expanded=False):
        st.code(json.dumps(clinical_data, indent=2, ensure_ascii=False), language="json")

    # --- Cleanup: remove the temp file ---
    try:
        os.remove(temp_path)
    except OSError:
        pass  # Not critical if cleanup fails

    st.divider()
    st.markdown(
        "<p style='text-align:center; color:#555;'>✅ Processing complete.</p>",
        unsafe_allow_html=True,
    )

else:
    # Placeholder when no file is uploaded yet
    st.markdown(
        """
        <div style="text-align:center; padding:3rem; color:#555;">
            <p style="font-size:3rem;">🎤</p>
            <p>Upload a German medical dictation to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
