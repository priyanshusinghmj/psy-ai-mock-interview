from pydantic import BaseModel, ConfigDict, Field
from app.schemas.interview import QuestionType

class GeneratedQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question_text: str = Field(min_length=10, max_length=1000)
    skill: str = Field(min_length=1, max_length=100)
    question_type: QuestionType