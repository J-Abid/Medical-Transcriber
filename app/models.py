"""Pydantic models for structured clinical output."""

from pydantic import BaseModel, Field


class ClinicalSummary(BaseModel):
    """Structured clinical summary extracted from a medical dictation."""

    patient_complaint: str = Field(
        description="Chief complaint or reason for visit, in the patient's terms."
    )
    findings: str = Field(
        description="Clinical findings from examination or history."
    )
    diagnosis: str = Field(
        description="Working or confirmed diagnosis."
    )
    next_steps: str = Field(
        description="Recommended next steps: treatment, referrals, follow-up."
    )
