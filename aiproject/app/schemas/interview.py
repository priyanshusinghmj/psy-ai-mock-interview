from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.scoring import ScoreBreakdown
from app.schemas.evaluation import EvaluationResult

class InterviewStatus(str, Enum):
    CREATED = "CREATED"
    ACTIVE = "ACTIVE"
    TERMINATED = "TERMINATED"
    COMPLETED = "COMPLETED"

class QuestionType(str, Enum):
    TECHNICAL = "TECHNICAL"
    BEHAVIORAL = "BEHAVIORAL"
    CONCEPTUAL = "CONCEPTUAL"
    SCENARIO = "SCENARIO"

class DifficultyTier(int, Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4

class CandidateProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    candidate_name: str | None = None
    skills: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    experience_years: float = 0
    resume_summary: str | None = None

class JDProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role_title: str
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    experience_required: float = 0
    responsibilities: list[str] = Field(default_factory=list)
    jd_summary: str | None = None

class InterviewQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question_id: str
    question_text: str
    skill: str
    question_type: QuestionType
    difficulty: DifficultyTier
    created_at: datetime

class CandidateAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question_id: str
    answer_text: str
    response_time_seconds: float = Field(..., ge=0)
    submitted_at: datetime

class InterviewTurn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: InterviewQuestion
    answer: CandidateAnswer | None = None
    score: ScoreBreakdown | None = None
    total_score: float | None = None
    evaluation: EvaluationResult | None = None

class InterviewMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    total_questions: int = 0
    answered_questions: int = 0
    average_score: float = 0
    highest_score: float = 0
    lowest_score: float = 0

class InterviewState(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    interview_id: str
    status: InterviewStatus = InterviewStatus.CREATED
    candidate_profile: CandidateProfile
    jd_profile: JDProfile
    difficulty: DifficultyTier = DifficultyTier.EASY
    question_number: int = 0
    current_skill: str | None = None
    current_question: InterviewQuestion | None = None
    history: list[InterviewTurn] = Field(default_factory=list)
    scores: list[float] = Field(default_factory=list)
    average_score: float = 0
    termination_flag: bool = False
    termination_reason: str | None = None
    awaiting_question: bool = True
    started_at: datetime
    completed_at: datetime | None = None
    metrics: InterviewMetrics = Field(default_factory=InterviewMetrics)