from pydantic import BaseModel, ConfigDict
from app.schemas.scoring import InterviewReadiness, SkillScore

class InterviewReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    readiness: InterviewReadiness
    skill_breakdown: list[SkillScore]
    strengths: list[str]
    weaknesses: list[str]
    actionable_feedback: list[str]
    total_questions: int
    average_score: float
    highest_score: float
    lowest_score: float
    hiring_recommendation: str