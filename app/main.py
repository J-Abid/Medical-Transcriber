"""CLI entry point for meddict."""

import json
import os
import sys
from pathlib import Path

import click

from app.extractor import extract_summary
from app.transcriber import transcribe


@click.command()
@click.argument("audio_file", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--model-size",
    default="small",
    help="Whisper model size (tiny, base, small, medium, large-v3).",
    show_default=True,
)
@click.option(
    "--transcript-only",
    is_flag=True,
    help="Output only the transcript, skip LLM extraction.",
)
@click.option(
    "--llm-model",
    default=lambda: os.environ.get("LLM_MODEL", "llama3.2"),
    help="LLM model name. [env: LLM_MODEL]",
    show_default="llama3.2",
)
def cli(
    audio_file: Path,
    model_size: str,
    transcript_only: bool,
    llm_model: str,
) -> None:
    """Transcribe a German medical dictation and extract a clinical summary."""
    # Step 1: Transcribe audio
    try:
        transcript = transcribe(audio_file, model_size=model_size)
    except FileNotFoundError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)

    click.echo(f"\n--- Transcript ---\n{transcript}\n", err=True)

    if transcript_only:
        click.echo(transcript)
        return

    # Step 2: Extract structured summary via LLM
    base_url = os.environ.get("LLM_BASE_URL", "http://localhost:11434/v1")
    api_key = os.environ.get("LLM_API_KEY", "ollama")

    try:
        summary = extract_summary(
            transcript,
            base_url=base_url,
            api_key=api_key,
            model=llm_model,
        )
    except (ValueError, Exception) as exc:
        click.echo(f"LLM extraction failed: {exc}", err=True)
        sys.exit(1)

    click.echo(summary.model_dump_json(indent=2))


if __name__ == "__main__":
    cli()
