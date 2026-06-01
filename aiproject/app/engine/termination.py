from app.engine.interview_rules import InterviewRules
from app.schemas.interview import InterviewTurn

def _has_consecutive_failures(history: list[InterviewTurn], rules: InterviewRules) -> bool:
    if len(history) < rules.consecutive_failure_count:
        return False

    recent_turns = history[-rules.consecutive_failure_count:]
    for turn in recent_turns:
        if turn.total_score is None:
            return False
        if turn.total_score >= rules.consecutive_failure_threshold:
            return False
    return True

def check_early_termination(
    history: list[InterviewTurn],
    question_number: int,
    average_score: float,
    rules: InterviewRules,
) -> tuple[bool, str | None]:
    if (
        question_number >= rules.minimum_questions_before_termination
        and average_score < rules.average_termination_threshold
    ):
        return (
            True,
            f"Interview terminated early due to low average score: {average_score:.2f}",
        )

    if _has_consecutive_failures(history, rules):
        return (
            True,
            f"Interview terminated early due to {rules.consecutive_failure_count} consecutive low responses.",
        )

    return False, None