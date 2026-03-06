"""
audio_processor.py — Speech-to-Text with Faster-Whisper
========================================================
Workflow:
  1. Load Model   →  Load the faster-whisper model (cached so it only loads once)
  2. Read Audio    →  Accept a file path to a WAV or MP3 file
  3. Transcribe    →  Run Whisper inference with language forced to German ("de")
  4. Return Text   →  Return the full transcription as a plain string

This module exposes two things:
  • load_model()      — returns a WhisperModel instance (cached)
  • transcribe_audio() — takes a file path, returns transcribed text
"""

from faster_whisper import WhisperModel

import config


# ---------------------------------------------------------------------------
# Step 1: Load Model
# ---------------------------------------------------------------------------
# We cache the model in a module-level variable so it is only loaded once
# across multiple transcription requests (saves time & memory).
_model: WhisperModel | None = None


def load_model() -> WhisperModel:
    """
    Load (or return the already-loaded) Whisper model.

    Uses settings from config.py:
      - WHISPER_MODEL_SIZE  (e.g. "small")
      - WHISPER_DEVICE      (e.g. "cpu")
      - WHISPER_COMPUTE_TYPE (e.g. "int8")
    """
    global _model

    if _model is None:
        print(
            f"[audio_processor] Loading Whisper model: "
            f"size={config.WHISPER_MODEL_SIZE}, "
            f"device={config.WHISPER_DEVICE}, "
            f"compute_type={config.WHISPER_COMPUTE_TYPE}"
        )
        _model = WhisperModel(
            model_size_or_path=config.WHISPER_MODEL_SIZE,
            device=config.WHISPER_DEVICE,
            compute_type=config.WHISPER_COMPUTE_TYPE,
        )
        print("[audio_processor] Model loaded successfully.")

    return _model


# ---------------------------------------------------------------------------
# Step 2–4: Read Audio → Transcribe → Return Text
# ---------------------------------------------------------------------------
def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file (WAV or MP3) to German text.

    Args:
        file_path: Path to the audio file on disk.

    Returns:
        The full transcription as a single string.

    Workflow:
        1. Ensure the model is loaded.
        2. Call model.transcribe() with language="de" (German).
        3. Iterate over the returned segments and join them.
        4. Return the combined text.
    """

    # 1. Make sure the model is ready
    model = load_model()

    # 2. Run transcription — language is forced to German
    #    beam_size=5 gives better accuracy at a small speed cost
    segments, info = model.transcribe(
        file_path,
        language=config.WHISPER_LANGUAGE,  # "de"
        beam_size=5,
    )

    print(
        f"[audio_processor] Detected language '{info.language}' "
        f"with probability {info.language_probability:.2f}"
    )

    # 3. Collect all segment texts into one list
    transcript_parts: list[str] = []
    for segment in segments:
        # Each segment has: start, end, text
        transcript_parts.append(segment.text.strip())

    # 4. Join everything into a single string and return
    full_text = " ".join(transcript_parts)
    print(f"[audio_processor] Transcription complete ({len(full_text)} chars).")

    return full_text
