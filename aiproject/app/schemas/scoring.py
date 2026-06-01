# app/schemas/scoring.py
from pydantic import BaseModel, Field, ConfigDict

class ScoreBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")

    accuracy: float = Field(..., ge=0, le=25)
    clarity: float = Field(..., ge=0, le=20)
    depth: float = Field(..., ge=0, le=25)
    relevance: float = Field(..., ge=0, le=20)
    time_efficiency: float = Field(..., ge=0, le=10)

    @property
    def total(self) -> float:
        return (
            self.accuracy
            + self.clarity
            + self.depth
            + self.relevance
            + self.time_efficiency
        )

class SkillScore(BaseModel):
    model_config = ConfigDict(extra="forbid")
    skill_name: str
    average_score: float = Field(..., ge=0, le=100)
    questions_attempted: int = Field(default=0, ge=0)

class InterviewReadiness(BaseModel):
    model_config = ConfigDict(extra="forbid")
    technical_score: float = Field(..., ge=0, le=100)
    behavioral_score: float = Field(..., ge=0, le=100)
    scenario_score: float = Field(..., ge=0, le=100)
    communication_score: float = Field(..., ge=0, le=100)
    readiness_score: float = Field(..., ge=0, le=100)
    readiness_label: str