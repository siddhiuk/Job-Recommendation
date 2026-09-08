from .semantic_similarity import calculate_similarity
from .resume_matching import calculate_skill_match


def recommend_jobs(resume_text, resume_skills, jobs):

    recommendations = []

    for _, job in jobs.iterrows():

        job_skills = [
            skill.strip()
            for skill in job["skills"].split(",")
        ]

        semantic_score = calculate_similarity(
            resume_text,
            job["description"]
        )

        skill_score, matched, missing = calculate_skill_match(
            resume_skills,
            job_skills
        )

        final_score = (
            0.6 * semantic_score +
            0.4 * skill_score
        )

        recommendations.append({

            "job_title": job["job_title"],

            "semantic_score":
                round(semantic_score * 100, 2),

            "skill_score":
                round(skill_score * 100, 2),

            "final_score":
                round(final_score * 100, 2),

            "matched_skills":
                matched,

            "missing_skills":
                missing
        })

    recommendations.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return recommendations[:5]