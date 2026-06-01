from openai import AsyncOpenAI
from app.schemas.evaluation import EvaluationResult
from app.services.evaluator import EvaluationProvider

class OpenAIEvaluationProvider(EvaluationProvider):
    def __init__(self, client: AsyncOpenAI, model: str) -> None:
        self.client = client
        self.model = model

    async def evaluate(self, system_prompt: str, user_prompt: str) -> EvaluationResult:
        completion = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=EvaluationResult,
            temperature=0.1,
        )
        parsed = completion.choices[0].message.parsed
        if parsed is None:
            raise ValueError("OpenAI failed to output parsed structured evaluation metadata.")
        return parsed