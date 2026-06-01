from app.schemas.interview import InterviewState

class MemoryInterviewRepository:
    def __init__(self) -> None:
        self._store: dict[str, InterviewState] = {}

    async def save(self, state: InterviewState) -> None:
        self._store[state.interview_id] = state

    async def get(self, interview_id: str) -> InterviewState | None:
        return self._store.get(interview_id)