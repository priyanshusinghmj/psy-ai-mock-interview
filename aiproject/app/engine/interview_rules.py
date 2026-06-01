from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class InterviewRules:
    strong_response_threshold: float = 80.0
    weak_response_threshold: float = 40.0
    minimum_questions_before_termination: int = 5
    average_termination_threshold: float = 30.0
    consecutive_failure_threshold: float = 25.0
    consecutive_failure_count: int = 3
    max_questions: int = 10
    max_time_per_question_seconds: int = 60