from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException

from app.api.models import CreateInterviewRequest, SubmitAnswerRequest
from app.core.config import DEFAULT_INTERVIEW_RULES
from app.core.llm import evaluator, question_generator
from app.engine.state_manager import process_answer
from app.repositories.memory_repository import MemoryInterviewRepository
from app.schemas.interview import CandidateAnswer, InterviewState, InterviewStatus, DifficultyTier
from app.services.mock_parsers import parse_jd, parse_resume
from app.services.report_generator import ReportGenerator

router = APIRouter(prefix="/interviews", tags=["interviews"])
repo = MemoryInterviewRepository()
report_engine = ReportGenerator()

@router.post("")
async def create_interview(request: CreateInterviewRequest):
    candidate = parse_resume(request.resume_text)
    jd = parse_jd(request.jd_text)

    state = InterviewState(
        interview_id=str(uuid4()),
        status=InterviewStatus.ACTIVE,
        candidate_profile=candidate,
        jd_profile=jd,
        difficulty=DifficultyTier.EASY,
        started_at=datetime.utcnow(),
    )
    await repo.save(state)
    return state

@router.post("/{interview_id}/next-question")
async def next_question(interview_id: str):
    state = await repo.get(interview_id)
    if not state: raise HTTPException(status_code=404, detail="Session not found.")
    if state.status in (InterviewStatus.TERMINATED, InterviewStatus.COMPLETED):
        raise HTTPException(status_code=400, detail="Interview is no longer active.")
    
    if not state.awaiting_question and state.current_question is not None:
        return state.current_question

    question = await question_generator.generate_question(state)
    state.current_question = question
    state.awaiting_question = False

    await repo.save(state)
    return question

@router.post("/answer")
async def submit_answer(request: SubmitAnswerRequest):
    state = await repo.get(request.interview_id)
    if not state: raise HTTPException(status_code=404, detail="Session not found.")
    if state.current_question is None: raise HTTPException(status_code=400, detail="No active question available.")

    candidate_answer = CandidateAnswer(
        question_id=state.current_question.question_id,
        answer_text=request.answer_text,
        response_time_seconds=request.response_time_seconds,
        submitted_at=datetime.utcnow(),
    )

    evaluation = await evaluator.evaluate_answer(
        question=state.current_question.question_text,
        skill=state.current_question.skill,
        difficulty=state.current_question.difficulty.name,
        answer=candidate_answer.answer_text,
        response_time_seconds=candidate_answer.response_time_seconds,
        max_time_seconds=DEFAULT_INTERVIEW_RULES.max_time_per_question_seconds,
    )

    updated_state = process_answer(
        state=state,
        answer=candidate_answer,
        evaluation_result=evaluation,
        rules=DEFAULT_INTERVIEW_RULES,
    )
    await repo.save(updated_state)
    return updated_state

@router.get("/{interview_id}/report")
async def get_report(interview_id: str):
    state = await repo.get(interview_id)
    if not state: raise HTTPException(status_code=404, detail="Session not found.")
    return report_engine.generate(state)