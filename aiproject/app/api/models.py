from pydantic import BaseModel, ConfigDict

class CreateInterviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    resume_text: str
    jd_text: str

class SubmitAnswerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    interview_id: str
    answer_text: str
    response_time_seconds: float