from datetime import datetime
from uuid import uuid4
from openai import AsyncOpenAI
from app.schemas.interview import InterviewQuestion, InterviewState
from app.schemas.question_generation import GeneratedQuestion

QUESTION_SYSTEM_PROMPT = """
You are an expert technical interviewer. Generate exactly ONE interview question.
Target the specific skill requested and match the requested difficulty level tier rules.
"""

class QuestionGeneratorService:
    def __init__(self, client: AsyncOpenAI, model: str):
        self.client = client
        self.model = model

    async def generate_question(self, state: InterviewState) -> InterviewQuestion:
        # Use simple round-robin skill rotation to enforce coverage safety metrics
        skills = state.jd_profile.required_skills or state.candidate_profile.skills or ["Python"]
        selected_skill = skills[state.question_number % len(skills)]

        prompt = f"ROLE: {state.jd_profile.role_title}\nTARGET SKILL: {selected_skill}\nDIFFICULTY TIER LEVEL: {state.difficulty.value}"
        
        completion = await self.client.beta.chat.completions.parse(
            model=self.model,
            temperature=0.4,
            messages=[
                {"role": "system", "content": QUESTION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format=GeneratedQuestion,
        )
        
        generated = completion.choices[0].message.parsed
        if generated is None:
            raise ValueError("Failed to generate structural question.")

        return InterviewQuestion(
            question_id=str(uuid4()),
            question_text=generated.question_text,
            skill=generated.skill,
            question_type=generated.question_type,
            difficulty=state.difficulty,
            created_at=datetime.utcnow(),
        )