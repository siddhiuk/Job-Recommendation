import re


def generate_resume_suggestions(resume_text, skills):
    """
    Analyze a resume and generate improvement suggestions.
    """

    suggestions = []

    if not resume_text:
        return suggestions

    text = resume_text.lower()


    # --------------------------------------------------
    # 1. Email Check
    # --------------------------------------------------

    has_email = bool(
        re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            resume_text
        )
    )

    if not has_email:

        suggestions.append(
            "Add a professional email address to your resume."
        )


    # --------------------------------------------------
    # 2. Phone Number Check
    # --------------------------------------------------

    has_phone = bool(
        re.search(
            r"\b\d{10}\b",
            resume_text
        )
    )

    if not has_phone:

        suggestions.append(
            " Add a valid phone number to your resume."
        )


    # --------------------------------------------------
    # 3. Skills Check
    # --------------------------------------------------

    if len(skills) < 5:

        suggestions.append(
            " Add more relevant technical skills "
            "to improve your resume's skill coverage."
        )


    # --------------------------------------------------
    # 4. Education Section
    # --------------------------------------------------

    if "education" not in text:

        suggestions.append(
            " Add an Education section with your degree, "
            "college and academic details."
        )


    # --------------------------------------------------
    # 5. Experience Section
    # --------------------------------------------------

    if "experience" not in text:

        suggestions.append(
            " Add an Experience or Internship section "
            "if you have relevant experience."
        )


    # --------------------------------------------------
    # 6. Projects Section
    # --------------------------------------------------

    if "project" not in text:

        suggestions.append(
            " Add a Projects section describing "
            "your important academic or personal projects."
        )


    # --------------------------------------------------
    # 7. Certifications Section
    # --------------------------------------------------

    if "certification" not in text:

        suggestions.append(
            " Add a Certifications section for "
            "relevant courses and certifications."
        )


    # --------------------------------------------------
    # 8. Technical Keywords
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


    if technical_count < 3:

        suggestions.append(
            " Include more relevant technical keywords "
            "based on the jobs you are targeting."
        )


    # --------------------------------------------------
    # 9. Resume Length
    # --------------------------------------------------

    word_count = len(
        resume_text.split()
    )

    if word_count < 100:

        suggestions.append(
            "Your resume contains very little text. "
            "Add relevant education, projects, skills "
            "or experience details."
        )


    # --------------------------------------------------
    # No Suggestions
    # --------------------------------------------------

    if not suggestions:

        suggestions.append(
            " Your resume covers the major ATS-friendly "
            "sections and information."
        )


    return suggestions