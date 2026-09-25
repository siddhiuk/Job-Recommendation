import re


def calculate_ats_score(resume_text, skills):
    """
    Calculate an ATS-style resume score out of 100.

    Score components:
    - Resume length/content
    - Skills
    - Contact information
    - Section keywords
    - Technical keywords
    """

    if not resume_text:
        return 0

    text = resume_text.lower()

    score = 0


    # --------------------------------------------------
    # 1. Resume Content
    # --------------------------------------------------

    word_count = len(
        resume_text.split()
    )

    if word_count >= 300:
        score += 20

    elif word_count >= 200:
        score += 15

    elif word_count >= 100:
        score += 10

    elif word_count >= 50:
        score += 5


    # --------------------------------------------------
    # 2. Skills
    # --------------------------------------------------

    skill_count = len(skills)

    if skill_count >= 10:
        score += 25

    elif skill_count >= 7:
        score += 20

    elif skill_count >= 5:
        score += 15

    elif skill_count >= 3:
        score += 10

    elif skill_count >= 1:
        score += 5


    # --------------------------------------------------
    # 3. Contact Information
    # --------------------------------------------------

    has_email = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            resume_text
        )
    )

    has_phone = bool(
        re.search(
            r"\b\d{10}\b",
            resume_text
        )
    )

    if has_email:
        score += 10

    if has_phone:
        score += 10


    # --------------------------------------------------
    # 4. Important Resume Sections
    # --------------------------------------------------

    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications"
    ]

    section_count = 0

    for section in sections:

        if section in text:
            section_count += 1


    score += min(
        section_count * 4,
        20
    )


    # --------------------------------------------------
    # 5. Technical Keywords
    # --------------------------------------------------

    technical_keywords = [
        "python",
        "java",
        "sql",
        "machine learning",
        "artificial intelligence",
        "data science",
        "react",
        "javascript",
        "html",
        "css",
        "git",
        "github",
        "docker",
        "aws",
        "azure",
        "pandas",
        "numpy"
    ]

    technical_count = 0

    for keyword in technical_keywords:

        if keyword in text:
            technical_count += 1


    score += min(
        technical_count * 1,
        15
    )


    # --------------------------------------------------
    # Final Score
    # --------------------------------------------------

    return min(
        score,
        100
    )