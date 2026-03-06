# <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Stethoscope.png" alt="Stethoscope" width="40" /> Medical Transcriber

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0D0D0D)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=0D0D0D)
![Whisper](https://img.shields.io/badge/Faster--Whisper-STT-FF6B00?style=for-the-badge&logo=openai&logoColor=white&labelColor=0D0D0D)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0D0D0D)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge&labelColor=0D0D0D)

<br/>

**🎙️ German Medical Dictation → 📝 Transcription → 🧠 Structured Clinical JSON**

<br/>

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700">

</div>

CLI tool that transcribes German medical audio and extracts a structured clinical summary using a local LLM.

## Architecture

```
Audio (WAV/MP3)
  → faster-whisper (Whisper small, German, CPU)
    → Transcript
      → LLM (Ollama / OpenAI-compatible API)
        → Structured JSON (ClinicalSummary)
```

## Output Schema

```json
{
  "patient_complaint": "...",
  "findings": "...",
  "diagnosis": "...",
  "next_steps": "..."
}
```

---

## Local Setup (uv)

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Ollama](https://ollama.com/) (or any OpenAI-compatible API)
- ffmpeg (`brew install ffmpeg` / `apt install ffmpeg`)

### Install & Run

```bash
# Install dependencies
uv sync

# Pull a local LLM (default: llama3.2)
ollama pull llama3.2

# Run
uv run meddict recording.wav

# Transcript only (skip LLM)
uv run meddict recording.wav --transcript-only

# Use a different Whisper model
uv run meddict recording.wav --model-size tiny

# Pipe JSON to jq
uv run meddict recording.wav 2>/dev/null | jq .diagnosis
```

### Environment Variables

| Variable        | Default                         | Description              |
|-----------------|---------------------------------|--------------------------|
| `LLM_BASE_URL`  | `http://localhost:11434/v1`     | LLM API endpoint         |
| `LLM_API_KEY`   | `ollama`                        | API key                  |
| `LLM_MODEL`     | `llama3.2`                      | Model name               |

#### Example: Using OpenAI instead of Ollama

```bash
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_API_KEY="sk-..."
export LLM_MODEL="gpt-4o-mini"
uv run meddict recording.wav
```

---

## Docker Setup

### Build

```bash
docker build -t meddict .
```

### Run

The container needs network access to reach Ollama (or another LLM API).

```bash
# With Ollama running on the host
docker run --rm \
  --network host \
  -v ./recording.wav:/tmp/recording.wav \
  meddict /tmp/recording.wav

# With OpenAI API
docker run --rm \
  -e LLM_BASE_URL="https://api.openai.com/v1" \
  -e LLM_API_KEY="sk-..." \
  -e LLM_MODEL="gpt-4o-mini" \
  -v ./recording.wav:/tmp/recording.wav \
  meddict /tmp/recording.wav
```

---

## Project Structure

```
├── pyproject.toml       # uv project config & dependencies
├── Dockerfile           # Container build
├── README.md
├── app/
│   ├── __init__.py
│   ├── main.py          # CLI entry point (Click)
│   ├── models.py        # Pydantic schema (ClinicalSummary)
│   ├── transcriber.py   # faster-whisper wrapper
│   └── extractor.py     # LLM prompt + JSON parsing
```

## Design Decisions

- **faster-whisper** over openai-whisper: ~4× faster on CPU via CTranslate2
- **Whisper `small`**: best accuracy/speed tradeoff for German medical terms
- **OpenAI-compatible client**: works with Ollama, vLLM, OpenAI, Azure — swap via env vars
- **Pydantic validation**: catches malformed LLM output before it reaches the caller
- **stderr for logs, stdout for JSON**: clean for piping (`meddict audio.wav | jq`)

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<div align="center">

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="700">

<br/>

**Made with 🧡 for the medical community**

<br/>

![Star](https://img.shields.io/github/stars/your-username/medical-transcriber?style=social)

</div>
