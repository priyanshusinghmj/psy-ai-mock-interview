from typing import Protocol
from app.schemas.evaluation import EvaluationResult

SYSTEM_PROMPT = """
You are an objective technical interview evaluator. Your sole job is to score a candidate's response against the metric criteria.
Scoring Rubric:
- Accuracy (0-25)
- Clarity (0-20)
- Depth (0-25)
- Relevance (0-20)
(Time Efficiency will be evaluated purely deterministically by the system core).
"""

def build_evaluation_prompt(*, question: str, skill: str, difficulty: str, answer: str) -> str:
    return f"QUESTION: {question}\nSKILL: {skill}\nDIFFICULTY: {difficulty}\nANSWER: {answer}"

def calculate_time_score(response_time: float, max_time: int) -> float:
    if max_time <= 0: return 0
    ratio = response_time / max_time
    if ratio <= 0.50: return 10
    if ratio <= 0.75: return 8
    if ratio <= 1.00: return 6
    if ratio <= 1.25: return 3
    return 0

def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))

def sanitize_evaluation(result: EvaluationResult, response_time: float, max_time: int) -> EvaluationResult:
    result.score.accuracy = clamp(result.score.accuracy, 0, 25)
    result.score.clarity = clamp(result.score.clarity, 0, 20)
    result.score.depth = clamp(result.score.depth, 0, 25)
    result.score.relevance = clamp(result.score.relevance, 0, 20)
    result.score.time_efficiency = calculate_time_score(response_time, max_time)
    return result

class EvaluationProvider(Protocol):
    async def evaluate(self, system_prompt: str, user_prompt: str) -> EvaluationResult: ...

class EvaluatorService:
    def __init__(self, provider: EvaluationProvider):
        self.provider = provider

    async def evaluate_answer(
        self, *, question: str, skill: str, difficulty: str, answer: str, response_time_seconds: float, max_time_seconds: int
    ) -> EvaluationResult:
        user_prompt = build_evaluation_prompt(question=question, skill=skill, difficulty=difficulty, answer=answer)
        result = await self.provider.evaluate(SYSTEM_PROMPT, user_prompt)
        return sanitize_evaluation(result, response_time_seconds, max_time_seconds)