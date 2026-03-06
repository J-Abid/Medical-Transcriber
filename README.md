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

---

## ✨ What It Does

| Step | Component | Description |
|------|-----------|-------------|
| 1️⃣ | **Upload** | Upload a WAV or MP3 file with a German medical dictation |
| 2️⃣ | **Transcribe** | Local [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) model converts speech → German text |
| 3️⃣ | **Extract** | An LLM (OpenAI / Ollama / vLLM) extracts structured clinical data |
| 4️⃣ | **Display** | Beautiful dark-themed UI shows transcription + JSON results |

### 📋 Extracted JSON Fields

```json
{
  "patient_complaint": "Kopfschmerzen seit drei Tagen",
  "findings": "Blutdruck 140/90, leichte Nackensteifigkeit",
  "diagnosis": "Spannungskopfschmerz",
  "next_steps": "Ibuprofen 400mg, Kontrolle in einer Woche"
}
```

---

## 🏗️ Project Structure

```
medical_transcriber/
├── 🎯 app.py               # Streamlit UI — dark orange theme, file upload, display
├── 🎙️ audio_processor.py    # Whisper STT — load model, transcribe German audio
├── 🧠 llm_extractor.py      # LLM client — prompt engineering, JSON extraction
├── ⚙️ config.py              # Central config — model sizes, API URLs, keys
├── 🐳 Dockerfile            # Container build — uv + ffmpeg + Streamlit
├── 📦 pyproject.toml        # Dependencies for uv / pip
├── 🙈 .gitignore            # Ignore caches, models, env files
└── 📖 README.md             # You are here!
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **ffmpeg** installed on your system (`apt install ffmpeg` / `brew install ffmpeg`)
- An LLM server running (e.g., [Ollama](https://ollama.com/) with `ollama run mistral`)

---

### 🖥️ Option 1: Local Setup with `uv`

<details>
<summary><b>Click to expand step-by-step instructions</b></summary>

<br/>

**1. Install `uv`** (if you don't have it):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Clone and enter the project:**

```bash
git clone https://github.com/your-username/medical-transcriber.git
cd medical-transcriber
```

**3. Create a virtual environment and install dependencies:**

```bash
uv venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
uv pip install -e .
```

**4. Start your LLM server** (example with Ollama):

```bash
ollama run mistral
```

**5. Run the app:**

```bash
streamlit run app.py
```

**6. Open your browser** at [http://localhost:8501](http://localhost:8501) 🎉

</details>

---

### 🐳 Option 2: Docker Setup

<details>
<summary><b>Click to expand step-by-step instructions</b></summary>

<br/>

**1. Build the image:**

```bash
docker build -t medical-transcriber .
```

**2. Run the container:**

```bash
# Basic run:
docker run -p 8501:8501 medical-transcriber

# With custom LLM settings (e.g., pointing to host Ollama):
docker run -p 8501:8501 \
  -e LLM_BASE_URL="http://host.docker.internal:11434/v1" \
  -e LLM_MODEL_NAME="mistral" \
  medical-transcriber
```

**3. Open your browser** at [http://localhost:8501](http://localhost:8501) 🎉

</details>

---

## ⚙️ Configuration

All settings are controlled via **environment variables** or by editing `config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `WHISPER_MODEL_SIZE` | `small` | Whisper model: `tiny`, `base`, `small`, `medium`, `large-v3` |
| `WHISPER_DEVICE` | `cpu` | Compute device: `cpu` or `cuda` |
| `WHISPER_COMPUTE_TYPE` | `int8` | Precision: `int8`, `float16`, `float32` |
| `LLM_BASE_URL` | `http://localhost:11434/v1` | OpenAI-compatible API endpoint |
| `LLM_API_KEY` | `ollama` | API key (use any placeholder for local servers) |
| `LLM_MODEL_NAME` | `mistral` | Model name served by the LLM backend |
| `LLM_TEMPERATURE` | `0.1` | Lower = more deterministic output |
| `LLM_MAX_TOKENS` | `1024` | Maximum response length |

### 💡 Examples

**Use OpenAI GPT-4o-mini:**
```bash
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_API_KEY="sk-your-key-here"
export LLM_MODEL_NAME="gpt-4o-mini"
```

**Use a local vLLM server:**
```bash
export LLM_BASE_URL="http://localhost:8000/v1"
export LLM_API_KEY="not-needed"
export LLM_MODEL_NAME="mistralai/Mistral-7B-Instruct-v0.3"
```

---

## 🎨 UI Preview

The app uses a custom **Dark Mode** theme with an **Orange & Black** color palette:

- 🖤 Deep black background (`#0D0D0D`)
- 🟠 Vibrant orange accents (`#FF6B00`)
- Glowing buttons and dashed upload borders
- Clean card-based layout for extracted clinical data

---

## 🛠️ Tech Stack

<div align="center">

| Component | Technology |
|-----------|-----------|
| 🖥️ Frontend | Streamlit |
| 🎙️ Speech-to-Text | Faster-Whisper (CTranslate2) |
| 🧠 LLM Client | OpenAI Python SDK |
| 📦 Package Manager | uv |
| 🐳 Container | Docker |
| 🐍 Language | Python 3.12 |

</div>

---

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
