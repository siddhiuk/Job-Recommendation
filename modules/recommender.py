import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def clean_text(text):
    """Convert text to lowercase and normalize common skill variations."""

    if pd.isna(text):
        return ""

    text = str(text).lower()

    # Normalize common skill aliases
    aliases = {
        "scikit-learn": "scikit learn",
        "scikit.learn": "scikit learn",
        "reactjs": "react",
        "react.js": "react",
        "nodejs": "node.js",
        "node js": "node.js",
        "microsoft azure": "azure",
        "amazon web services": "aws",
        "google cloud platform": "google cloud",
        "gcp": "google cloud",
        "powerbi": "power bi",
        "machine-learning": "machine learning",
        "deep-learning": "deep learning",
        "artificial-intelligence": "artificial intelligence",
        "cybersecurity": "cyber security"
    }

    for alias, standard in aliases.items():
        text = text.replace(alias, standard)

    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def calculate_semantic_similarity(
    resume_text,
    resume_skills,
    job_title,
    job_skills,
    job_description
):
    """Calculate TF-IDF similarity using resume skills and complete job information."""

    resume_text = clean_text(resume_text)
    job_title = clean_text(job_title)
    job_skills = clean_text(job_skills)
    job_description = clean_text(job_description)

    resume_skill_text = " ".join(
        clean_text(skill)
        for skill in resume_skills
    )

    enhanced_resume = (
        f"{resume_text} "
        f"{resume_skill_text} "
        f"{resume_skill_text}"
    )

    complete_job_text = (
        f"{job_title} "
        f"{job_skills} "
        f"{job_skills} "
        f"{job_description}"
    )

    if not enhanced_resume.strip() or not complete_job_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    tfidf_matrix = vectorizer.fit_transform(
        [enhanced_resume, complete_job_text]
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return similarity * 100


def calculate_skill_match(resume_skills, job_skills):
    """Calculate skill matching while preserving readable skill names."""

    # Create normalized → original mappings
    resume_skill_map = {
        clean_text(skill): skill
        for skill in resume_skills
        if skill
    }

    job_skill_map = {
        clean_text(skill): skill
        for skill in job_skills
        if skill
    }

    if not job_skill_map:
        return 0.0, [], []

    resume_normalized = set(resume_skill_map.keys())
    job_normalized = set(job_skill_map.keys())

    matched_normalized = resume_normalized.intersection(
        job_normalized
    )

    missing_normalized = job_normalized.difference(
        resume_normalized
    )

    # Use original names for display
    matched_skills = sorted(
        resume_skill_map[skill]
        for skill in matched_normalized
    )

    missing_skills = sorted(
        job_skill_map[skill]
        for skill in missing_normalized
    )

    skill_score = (
        len(matched_normalized)
        / len(job_normalized)
    ) * 100

    return (
        skill_score,
        matched_skills,
        missing_skills
    )

def extract_job_skills(skills_text):
    """Convert the job's skills column into a list of skills."""

    if pd.isna(skills_text):
        return []

    skills_text = str(skills_text)

    # Supports comma, semicolon and pipe-separated skills
    skills = re.split(r"[,;|]", skills_text)

    return [
        skill.strip()
        for skill in skills
        if skill.strip()
    ]


def recommend_jobs(resume_text, resume_skills, jobs_df, top_n=5):
    """
    Recommend jobs using:
    1. Semantic similarity
    2. Skill matching
    3. Weighted final score
    """

    if not resume_text or jobs_df.empty:
        return []

    required_columns = [
        "job_title",
        "skills",
        "description"
    ]

    for column in required_columns:
        if column not in jobs_df.columns:
            raise ValueError(
                f"jobs.csv must contain a '{column}' column."
            )

    recommendations = []

    for _, job in jobs_df.iterrows():

        job_title = str(job["job_title"])
        job_description = str(job["description"])

        # --------------------------------
        # Semantic Similarity
        # --------------------------------

        semantic_score = calculate_semantic_similarity(
            resume_text,
            resume_skills,
            job_title,
            str(job["skills"]),
            job_description
        )

        # --------------------------------
        # Skill Matching
        # --------------------------------

        job_skills = extract_job_skills(
            job["skills"]
        )

        skill_score, matched_skills, missing_skills = (
            calculate_skill_match(
                resume_skills,
                job_skills
            )
        )

        # --------------------------------
        # Final Weighted Score
        # --------------------------------

        final_score = (
            (semantic_score * 0.60) +
            (skill_score * 0.40)
        )

        recommendations.append({
            "job_title": job_title,
            "semantic_score": round(
                semantic_score, 2
            ),
            "skill_score": round(
                skill_score, 2
            ),
            "final_score": round(
                final_score, 2
            ),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    # Highest score first
    recommendations.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return recommendations[:top_n]