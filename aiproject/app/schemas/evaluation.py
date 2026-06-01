from pydantic import BaseModel, ConfigDict, Field
from app.schemas.scoring import ScoreBreakdown

class EvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: ScoreBreakdown
    accuracy_reason: str = Field(min_length=5, max_length=500)
    clarity_reason: str = Field(min_length=5, max_length=500)
    depth_reason: str = Field(min_length=5, max_length=500)
    relevance_reason: str = Field(min_length=5, max_length=500)
    time_reason: str = Field(min_length=5, max_length=500)
    overall_feedback: str = Field(min_length=10, max_length=1000)
    strengths: list[str]
    weaknesses: list[str]