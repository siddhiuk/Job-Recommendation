def calculate_skill_match(resume_skills, job_skills):

    resume_skills = {
        skill.lower().strip()
        for skill in resume_skills
    }

    job_skills = {
        skill.lower().strip()
        for skill in job_skills
    }

    if not job_skills:
        return 0, [], []

    matched_skills = resume_skills.intersection(job_skills)

    missing_skills = job_skills - resume_skills

    score = len(matched_skills) / len(job_skills)

    return (
        score,
        list(matched_skills),
        list(missing_skills)
    )