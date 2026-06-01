from uuid import uuid4
from datetime import datetime
from app.schemas.evaluation import EvaluationResult
from app.schemas.scoring import ScoreBreakdown
from app.schemas.interview import InterviewQuestion, InterviewState, QuestionType
from app.schemas.question_generation import GeneratedQuestion

class MockEvaluatorService:
    async def evaluate_answer(
        self, *, question: str, skill: str, difficulty: str, answer: str, response_time_seconds: float, max_time_seconds: int
    ) -> EvaluationResult:
        from app.services.evaluator import calculate_time_score
        time_score = calculate_time_score(response_time_seconds, max_time_seconds)
        
        # Check if the user typed an actual response
        if len(answer.strip()) > 10 and "[No response" not in answer:
            # High mock values scaled to respect your Pydantic maximum thresholds
            return EvaluationResult(
                score=ScoreBreakdown(
                    accuracy=24.0,       # Max <= 25
                    clarity=19.0,        # Max <= 20
                    depth=23.0,          # Max <= 25
                    relevance=19.0,      # Max <= 20
                    time_efficiency=time_score if time_score > 0 else 10.0
                ),
                accuracy_reason="The response demonstrates excellent technical correctness and syntax awareness.",
                clarity_reason="The explanation was structured clearly and easy to follow.",
                depth_reason="Good conceptual insight shown regarding backend execution.",
                relevance_reason="Directly answered the target prompt effectively.",
                time_reason="Response submitted cleanly within the constraint window.",
                overall_feedback="Excellent performance! Demonstrated firm grasp of programming principles.",
                strengths=["Clear syntax mapping", "Direct explanation structural focus"],
                weaknesses=["Could expand slightly on edge-case memory allocation trade-offs"]
            )
        else:
            # Low scores for empty/timeout answers to safely test early termination
            return EvaluationResult(
                score=ScoreBreakdown(
                    accuracy=5.0, 
                    clarity=5.0, 
                    depth=5.0, 
                    relevance=5.0, 
                    time_efficiency=2.0
                ),
                accuracy_reason="No technical substance provided.",
                clarity_reason="Answer was missing or too short to evaluate.",
                depth_reason="No depth shown.",
                relevance_reason="Did not address the question.",
                time_reason="Timeout or skipped.",
                overall_feedback="Candidate did not provide enough detail.",
                strengths=[],
                weaknesses=["Missing core concepts"]
            )

class MockQuestionGeneratorService:
    def __init__(self):
        # Pool of 10 distinct technical backend questions so it won't repeat early
        self.question_pool = [
            "What is the difference between a list and a tuple in Python?",
            "How does dependency injection work natively inside FastAPI?",
            "Explain what causes an N+1 query problem in relational databases.",
            "How does the descriptor protocol function internally within Python?",
            "What is the purpose of Pydantic BaseModel validation in FastAPI?",
            "Explain the difference between synchronous and asynchronous tasks in Python.",
            "How do decorators work in Python, and when would you use one?",
            "What are database indexes, and how do they speed up search queries?",
            "Explain the difference between global and local variables in a program.",
            "What is a deadlock in Operating Systems, and how can it be prevented?"
        ]

    async def generate_question(self, state: InterviewState) -> InterviewQuestion:
        skills = state.jd_profile.required_skills or state.candidate_profile.skills or ["Python"]
        selected_skill = skills[state.question_number % len(skills)]
        
        # Select unique questions sequentially based on the active question count
        pool_index = (state.question_number - 1) % len(self.question_pool)
        question_text = self.question_pool[pool_index]
        
        return InterviewQuestion(
            question_id=str(uuid4()),
            question_text=question_text,
            skill=selected_skill,
            question_type=QuestionType.TECHNICAL,
            difficulty=state.difficulty,
            created_at=datetime.utcnow()
        )

evaluator = MockEvaluatorService()
question_generator = MockQuestionGeneratorService()