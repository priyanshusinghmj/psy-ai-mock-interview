from app.schemas.interview import CandidateProfile, JDProfile

def parse_resume(resume_text: str) -> CandidateProfile:
    return CandidateProfile(
        candidate_name="Priyanshu Singh Yadav",
        skills=["Python", "FastAPI", "SQL", "Java"],
        projects=["AI Mock Interviewer Platform"],
        experience_years=1.5,
        resume_summary=resume_text[:300],
    )

def parse_jd(jd_text: str) -> JDProfile:
    return JDProfile(
        role_title="Backend Software Engineer",
        required_skills=["Python", "FastAPI", "SQL"],
        jd_summary=jd_text[:300],
    )