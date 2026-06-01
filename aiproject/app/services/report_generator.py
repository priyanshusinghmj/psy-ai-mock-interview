from collections import Counter, defaultdict
from app.schemas.interview import InterviewState, QuestionType
from app.schemas.report import InterviewReport
from app.schemas.scoring import InterviewReadiness, SkillScore

def safe_average(values: list[float]) -> float:
    return round(sum(values) / len(values), 2) if values else 0.0

def get_hiring_label(score: float) -> str:
    if score >= 85: return "Strong Hire"
    if score >= 70: return "Hire"
    if score >= 55: return "Borderline"
    return "No Hire"

class ReportGenerator:
    def generate(self, state: InterviewState) -> InterviewReport:
        tech, behav, scen, comm = [], [], [], []
        skill_map = defaultdict(list)
        strengths, weaknesses, feedback = Counter(), Counter(), Counter()

        for turn in state.history:
            if turn.total_score is None or turn.score is None: continue
            
            skill_map[turn.question.skill].append(turn.total_score)
            
            if turn.question.question_type == QuestionType.TECHNICAL: tech.append(turn.total_score)
            elif turn.question.question_type == QuestionType.BEHAVIORAL: behav.append(turn.total_score)
            elif turn.question.question_type == QuestionType.SCENARIO: scen.append(turn.total_score)
            
            comm.append(turn.score.clarity * 5) # Scale to 100 base bounds

            if turn.evaluation:
                for s in turn.evaluation.strengths: strengths[s] += 1
                for w in turn.evaluation.weaknesses: weaknesses[w] += 1
                feedback[turn.evaluation.overall_feedback] += 1

        t_avg, b_avg, s_avg, c_avg = safe_average(tech), safe_average(behav), safe_average(scen), safe_average(comm)
        readiness_score = round(t_avg * 0.50 + b_avg * 0.20 + s_avg * 0.20 + c_avg * 0.10, 2)

        skills = [SkillScore(skill_name=k, average_score=safe_average(v), questions_attempted=len(v)) for k, v in skill_map.items()]

        return InterviewReport(
            readiness=InterviewReadiness(
                technical_score=t_avg, behavioral_score=b_avg, scenario_score=s_avg,
                communication_score=c_avg, readiness_score=readiness_score,
                readiness_label=get_hiring_label(readiness_score)
            ),
            skill_breakdown=skills,
            strengths=[i for i, _ in strengths.most_common(3)],
            weaknesses=[i for i, _ in weaknesses.most_common(3)],
            actionable_feedback=[i for i, _ in feedback.most_common(3)],
            total_questions=state.metrics.total_questions,
            average_score=state.metrics.average_score,
            highest_score=state.metrics.highest_score,
            lowest_score=state.metrics.lowest_score,
            hiring_recommendation=get_hiring_label(readiness_score)
        )