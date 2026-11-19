from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field

Severity = Literal["critical", "high", "medium", "low", "info"]

class Finding(BaseModel):
    category: str
    severity: Severity
    confidence: str
    parameter: str | None = None
    title: str
    evidence: str
    recommendation: str

class ScanReport(BaseModel):
    tool: str = "SQLSentinel"
    version: str = "1.0.0"
    target: str
    host: str
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: str | None = None
    requests_sent: int = 0
    parameters_tested: list[str] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
