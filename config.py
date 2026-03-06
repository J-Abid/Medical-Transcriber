"""
config.py — Central Configuration Hub
======================================
This file holds all configurable settings for the Medical Transcriber app.
Change values here instead of hunting through multiple files.

Sections:
  1. Whisper STT settings   (model size, device, compute type)
  2. LLM / OpenAI settings  (base URL, API key, model name)
  3. Application settings    (temp dir, allowed file types)
"""

import os

# ---------------------------------------------------------------------------
# 1. WHISPER STT SETTINGS
# ---------------------------------------------------------------------------
# Model size options: "tiny", "base", "small", "medium", "large-v2", "large-v3"
# Smaller = faster but less accurate. "small" is a good balance for German medical text.
WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "small")

# Device: "cpu" or "cuda" (GPU). Use "cpu" if no NVIDIA GPU is available.
WHISPER_DEVICE: str = os.getenv("WHISPER_DEVICE", "cpu")

# Compute type: "int8" (fast, lower memory) or "float16" (GPU) or "float32" (CPU precise)
WHISPER_COMPUTE_TYPE: str = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

# Force German language for transcription
WHISPER_LANGUAGE: str = "de"

# ---------------------------------------------------------------------------
# 2. LLM / OPENAI-COMPATIBLE SETTINGS
# ---------------------------------------------------------------------------
# Base URL — point this to OpenAI, Ollama, vLLM, or any compatible server.
#   • OpenAI:       "https://api.openai.com/v1"
#   • Ollama local: "http://localhost:11434/v1"
#   • vLLM local:   "http://localhost:8000/v1"
LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")

# API key — required for OpenAI; for local servers you can use any placeholder.
LLM_API_KEY: str = os.getenv("LLM_API_KEY", "ollama")

# Model name — must match what the server offers.
#   • OpenAI example:  "gpt-4o-mini"
#   • Ollama example:  "llama3"  or  "mistral"
LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "mistral")

# Temperature — lower = more deterministic (good for structured extraction)
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))

# Maximum tokens the LLM may generate in its response
LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))

# ---------------------------------------------------------------------------
# 3. APPLICATION SETTINGS
# ---------------------------------------------------------------------------
# Temporary directory for uploaded audio files
TEMP_AUDIO_DIR: str = os.getenv("TEMP_AUDIO_DIR", "/tmp/medical_audio")

# Allowed upload extensions (Streamlit file_uploader types)
ALLOWED_EXTENSIONS: list[str] = ["wav", "mp3"]
