"""
llm_extractor.py — Structured Clinical Data Extraction via LLM
===============================================================
Workflow:
  1. Receive Text     →  Get the German transcription from the STT step
  2. Construct Prompt  →  Build a system + user prompt asking for JSON extraction
  3. Call LLM          →  Send the prompt to an OpenAI-compatible API
  4. Parse JSON        →  Extract and validate the JSON from the LLM response
  5. Return Output     →  Return a clean Python dict with the clinical fields

Required JSON output fields:
  • patient_complaint  — What the patient is complaining about
  • findings           — Clinical findings mentioned in the dictation
  • diagnosis          — The doctor's diagnosis
  • next_steps         — Recommended next steps / treatment plan
"""

import json
from openai import OpenAI

import config


# ---------------------------------------------------------------------------
# Step 2: Construct Prompt
# ---------------------------------------------------------------------------
# System prompt — tells the LLM *who* it is and *how* to respond.
SYSTEM_PROMPT = """\
Du bist ein erfahrener medizinischer Assistent.
Deine Aufgabe ist es, aus einem deutschsprachigen ärztlichen Diktat
strukturierte klinische Daten zu extrahieren.

Antworte AUSSCHLIESSLICH mit einem gültigen JSON-Objekt (kein Markdown,
kein zusätzlicher Text). Das JSON muss exakt diese vier Schlüssel enthalten:

{
  "patient_complaint": "...",
  "findings": "...",
  "diagnosis": "...",
  "next_steps": "..."
}

Regeln:
- Fasse die Informationen kurz und präzise zusammen.
- Wenn eine Kategorie im Diktat nicht erwähnt wird, setze den Wert auf "Nicht erwähnt".
- Antworte immer auf Deutsch.
"""

# User prompt template — the {transcription} placeholder is filled at runtime.
USER_PROMPT_TEMPLATE = """\
Hier ist das ärztliche Diktat:

\"\"\"
{transcription}
\"\"\"

Bitte extrahiere die klinischen Daten als JSON.
"""


# ---------------------------------------------------------------------------
# Step 1 + 3 + 4 + 5: Full extraction pipeline
# ---------------------------------------------------------------------------
def extract_clinical_data(transcription: str) -> dict:
    """
    Take a German medical transcription and return structured clinical data.

    Args:
        transcription: The raw German text from the Whisper STT step.

    Returns:
        A Python dict with keys:
          patient_complaint, findings, diagnosis, next_steps

    Raises:
        ValueError: If the LLM response cannot be parsed as valid JSON.
    """

    # --- Step 1: Receive text (it's the function argument) ---

    # --- Step 2: Construct the user prompt with the transcription ---
    user_prompt = USER_PROMPT_TEMPLATE.format(transcription=transcription)

    # --- Step 3: Call the LLM via OpenAI-compatible client ---
    #     The base_url and api_key come from config.py, so you can
    #     point this to OpenAI, Ollama, vLLM, or any compatible server.
    client = OpenAI(
        base_url=config.LLM_BASE_URL,
        api_key=config.LLM_API_KEY,
    )

    print(
        f"[llm_extractor] Calling LLM: model={config.LLM_MODEL_NAME}, "
        f"base_url={config.LLM_BASE_URL}"
    )

    response = client.chat.completions.create(
        model=config.LLM_MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=config.LLM_TEMPERATURE,
        max_tokens=config.LLM_MAX_TOKENS,
    )

    # Get the raw text content from the LLM response
    raw_content: str = response.choices[0].message.content.strip()
    print(f"[llm_extractor] Raw LLM response:\n{raw_content}")

    # --- Step 4: Parse JSON from the response ---
    clinical_data = _parse_json_response(raw_content)

    # --- Step 5: Return the clean dict ---
    print("[llm_extractor] Extraction complete.")
    return clinical_data


# ---------------------------------------------------------------------------
# Helper: Robust JSON parsing
# ---------------------------------------------------------------------------
def _parse_json_response(raw: str) -> dict:
    """
    Try to parse JSON from the LLM response.

    Some LLMs wrap JSON in ```json ... ``` code fences,
    so we strip those if present before parsing.
    """

    # Remove optional markdown code fences
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        # Remove first line (```json) and last line (```)
        lines = cleaned.split("\n")
        # Drop first and last lines that are just fences
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"The LLM did not return valid JSON. "
            f"Raw response:\n{raw}\n\nError: {exc}"
        )

    # Ensure all expected keys exist (fill missing ones with a default)
    expected_keys = ["patient_complaint", "findings", "diagnosis", "next_steps"]
    for key in expected_keys:
        if key not in data:
            data[key] = "Nicht erwähnt"

    return data
