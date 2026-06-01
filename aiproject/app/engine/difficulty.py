from app.engine.interview_rules import InterviewRules
from app.schemas.interview import DifficultyTier

def calculate_next_difficulty(
    current_difficulty: DifficultyTier,
    last_answer_score: float,
    rules: InterviewRules,
) -> DifficultyTier:
    difficulty_value = int(current_difficulty)

    if last_answer_score >= rules.strong_response_threshold:
        difficulty_value += 1
    elif last_answer_score <= rules.weak_response_threshold:
        difficulty_value -= 1

    difficulty_value = max(
        DifficultyTier.EASY.value,
        min(DifficultyTier.EXPERT.value, difficulty_value),
    )
    return DifficultyTier(difficulty_value)