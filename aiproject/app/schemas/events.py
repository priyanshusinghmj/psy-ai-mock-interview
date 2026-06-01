from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field

class EventType(str, Enum):
    INTERVIEW_STARTED = "INTERVIEW_STARTED"
    RESUME_PARSED = "RESUME_PARSED"
    JD_PARSED = "JD_PARSED"
    QUESTION_GENERATED = "QUESTION_GENERATED"
    ANSWER_RECEIVED = "ANSWER_RECEIVED"
    SCORE_COMPUTED = "SCORE_COMPUTED"
    DIFFICULTY_UP = "DIFFICULTY_UP"
    DIFFICULTY_DOWN = "DIFFICULTY_DOWN"
    DIFFICULTY_UNCHANGED = "DIFFICULTY_UNCHANGED"
    TIMEOUT = "TIMEOUT"
    EARLY_TERMINATION = "EARLY_TERMINATION"
    INTERVIEW_COMPLETED = "INTERVIEW_COMPLETED"

class AuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    interview_id: str
    event_type: EventType
    timestamp: datetime
    payload: dict[str, Any] = Field(default_factory=dict)