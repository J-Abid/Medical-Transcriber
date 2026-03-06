"""LLM-based clinical summary extraction from transcripts."""

import json
import re
import sys

from openai import OpenAI

from app.models import ClinicalSummary


SYSTEM_PROMPT = """\
You are a medical documentation assistant specializing in German clinical language.

Given a transcript of a German medical dictation, extract a structured clinical summary.
Respond with ONLY a JSON object (no markdown fences, no extra text) using these exact keys:

{
  "patient_complaint": "...",
  "findings": "...",
  "diagnosis": "...",
  "next_steps": "..."
}

All values should be concise, in German, and clinically accurate.
If a field cannot be determined from the transcript, use "Nicht angegeben".
"""


def _strip_markdown_fences(text: str) -> str:
    """Remove ```json ... ``` wrappers that some LLMs add."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)
    return text.strip()


def extract_summary(
    transcript: str,
    base_url: str = "http://localhost:11434/v1",
    api_key: str = "ollama",
    model: str = "llama3.2",
) -> ClinicalSummary:
    """Send transcript to an OpenAI-compatible LLM and parse the response.

    Args:
        transcript: German medical dictation transcript.
        base_url: LLM API base URL (default: local Ollama).
        api_key: API key (use 'ollama' for local Ollama).
        model: Model identifier.

    Returns:
        Validated ClinicalSummary.
    """
    client = OpenAI(base_url=base_url, api_key=api_key)

    print(f"Sending transcript to LLM ({model})...", file=sys.stderr)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        temperature=0.2,
    )

    raw = response.choices[0].message.content or ""
    cleaned = _strip_markdown_fences(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned invalid JSON:\n{raw}"
        ) from exc

    return ClinicalSummary.model_validate(data)
