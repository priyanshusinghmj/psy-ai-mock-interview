from datetime import datetime
from app.engine.difficulty import calculate_next_difficulty
from app.engine.termination import check_early_termination
from app.engine.interview_rules import InterviewRules
from app.schemas.scoring import ScoreBreakdown
from app.schemas.evaluation import EvaluationResult
from app.schemas.interview import (
    CandidateAnswer,
    InterviewMetrics,
    InterviewState,
    InterviewStatus,
    InterviewTurn,
)

def recalculate_metrics(state: InterviewState) -> InterviewMetrics:
    scores = [turn.total_score for turn in state.history if turn.total_score is not None]
    if not scores:
        return InterviewMetrics()

    return InterviewMetrics(
        total_questions=len(state.history),
        answered_questions=len(state.history),
        average_score=sum(scores) / len(scores),
        highest_score=max(scores),
        lowest_score=min(scores),
    )

def process_answer(
    state: InterviewState,
    answer: CandidateAnswer,
    evaluation_result: EvaluationResult,
    rules: InterviewRules,
) -> InterviewState:
    if state.current_question is None:
        raise ValueError("No active question exists.")

    total_score = round(evaluation_result.score.total, 2)

    turn = InterviewTurn(
        question=state.current_question,
        answer=answer,
        score=evaluation_result.score,
        total_score=total_score,
        evaluation=evaluation_result
    )

    state.history.append(turn)
    state.scores.append(total_score)
    state.question_number += 1

    state.metrics = recalculate_metrics(state)
    state.average_score = state.metrics.average_score

    state.difficulty = calculate_next_difficulty(
        current_difficulty=state.difficulty,
        last_answer_score=total_score,
        rules=rules,
    )

    terminate, reason = check_early_termination(
        history=state.history,
        question_number=state.question_number,
        average_score=state.average_score,
        rules=rules,
    )

    state.termination_flag = terminate
    state.termination_reason = reason

    if terminate or state.question_number >= rules.max_questions:
        state.status = InterviewStatus.TERMINATED if terminate else InterviewStatus.COMPLETED
        state.completed_at = datetime.utcnow()
        state.current_question = None
        state.awaiting_question = False
        return state

    state.current_question = None
    state.awaiting_question = True
    return state