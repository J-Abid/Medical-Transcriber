"""Audio transcription using faster-whisper (CTranslate2)."""

import sys
from pathlib import Path

from faster_whisper import WhisperModel


DEFAULT_MODEL_SIZE = "small"


def transcribe(
    audio_path: Path,
    model_size: str = DEFAULT_MODEL_SIZE,
) -> str:
    """Transcribe a German audio file to text.

    Args:
        audio_path: Path to WAV or MP3 file.
        model_size: Whisper model size (tiny, base, small, medium, large-v3).

    Returns:
        Full transcript as a single string.
    """
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    print(f"Loading Whisper model '{model_size}'...", file=sys.stderr)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    print("Transcribing...", file=sys.stderr)
    segments, info = model.transcribe(
        str(audio_path),
        language="de",
        beam_size=5,
        vad_filter=True,
    )

    transcript_parts: list[str] = []
    for segment in segments:
        transcript_parts.append(segment.text.strip())

    transcript = " ".join(transcript_parts)
    print(
        f"Transcription complete. Language: {info.language} "
        f"(probability {info.language_probability:.1%})",
        file=sys.stderr,
    )
    return transcript
