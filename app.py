import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Job Recommendation",
    layout="wide",
    initial_sidebar_state="expanded"
)



from modules.resume_parser import extract_text
from modules.ner import extract_skills, extract_entities
from modules.recommender import recommend_jobs
from modules.ats_score import calculate_ats_score
from modules.resume_improvement import generate_resume_suggestions
from modules.report_generator import generate_pdf_report

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Job Recommendation System",
    page_icon=" ",
    layout="wide"
)

# --------------------------------------------------
# Custom UI Styling
# --------------------------------------------------
st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    margin-bottom: 30px;
}

.section-title {
    font-size: 25px;
    font-weight: 650;
    margin-top: 25px;
    margin-bottom: 15px;
}

div[data-testid="stMetric"] {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(128, 128, 128, 0.25);
}

.job-card {
    padding: 20px;
    border-radius: 15px;
    border: 1px solid rgba(128, 128, 128, 0.25);
    margin-bottom: 20px;
}

.stTextInput > div > div > input {
    border-radius: 10px;
    padding: 10px 12px;
}

.stSlider {
    padding-top: 5px;
}



</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.markdown(
    '<div class="main-title">AI-Based Job Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your resume and get personalized job recommendations '
    'using NER, resume matching and semantic similarity.'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Load Jobs Dataset
# --------------------------------------------------

jobs = pd.read_csv("jobs.csv")


# --------------------------------------------------
# Resume Upload
# --------------------------------------------------

st.markdown(
    '<div class="section-title"> Upload Your Resume</div>',
    unsafe_allow_html=True
)

st.markdown(
    "Upload your PDF resume to analyze your skills, calculate your ATS score, "
    "and find suitable job opportunities."
)

uploaded_file = st.file_uploader(
    "Choose your resume (PDF)",
    type=["pdf"],
    help="Upload a PDF resume for analysis."
)



# --------------------------------------------------
# Resume Processing
# --------------------------------------------------

if uploaded_file:

    st.success("Resume uploaded successfully!")


    # Extract Resume Text

    resume_text = extract_text(uploaded_file)


    # --------------------------------------------------
    # Resume Preview
    # --------------------------------------------------

    st.subheader(" Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=200
    )




    # --------------------------------------------------
    # Skill Extraction
    # --------------------------------------------------

    skills = extract_skills(resume_text)

    st.subheader(" Skills Detected")

    if skills:

        st.write(", ".join(skills))

    else:

        st.warning(
            "No predefined technical skills detected."
        )

    # --------------------------------------------------
    # ATS Resume Score
    # --------------------------------------------------

    ats_score = calculate_ats_score(
        resume_text,
        skills
    )

    st.subheader(" Resume ATS Score")

    st.metric(
        "ATS Score",
        f"{ats_score}/100"
    )

    st.progress(
        min(ats_score / 100, 1.0)
    )

    if ats_score >= 80:

        st.success(
            " Strong ATS Score"
        )

    elif ats_score >= 60:

        st.info(
            " Good ATS Score"
        )

    elif ats_score >= 40:

        st.warning(
            "Your resume can be improved"
        )

    else:

        st.error(
            "Your resume needs significant improvement"
        )

    # --------------------------------------------------
    # Resume Improvement Suggestions
    # --------------------------------------------------

    suggestions = generate_resume_suggestions(
        resume_text,
        skills
    )

    st.subheader("Resume Improvement Suggestions")

    for suggestion in suggestions:
        st.write(
            suggestion
        )

    # --------------------------------------------------
    # Named Entities - Grouped by Classification
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">Named Entity Classification</div>',
        unsafe_allow_html=True
    )

    entities = extract_entities(resume_text)

    if entities:

        from collections import defaultdict
        import pandas as pd

        grouped_entities = defaultdict(list)

        for ent in entities:
            grouped_entities[ent["label"]].append(ent["text"])

        # Remove duplicate entities while preserving order
        for label in grouped_entities:
            grouped_entities[label] = list(
                dict.fromkeys(grouped_entities[label])
            )

        # Create one column for each classification
        entity_table = pd.DataFrame(
            dict(
                (label, pd.Series(values))
                for label, values in grouped_entities.items()
            )
        )

        st.dataframe(
            entity_table,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No named entities detected.")

    # --------------------------------------------------
    # Find Best Jobs Button
    # --------------------------------------------------

    if st.button(" Find Best Jobs"):

        with st.spinner(
            "Analyzing resume and matching jobs..."
        ):

            recommendations = recommend_jobs(
                resume_text,
                skills,
                jobs,
                top_n=len(jobs)
            )


        # --------------------------------------------------
        # Job Recommendations
        # --------------------------------------------------
        # --------------------------------------------------
        # Job Recommendation Dashboard
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Recommendation Dashboard</div>',
            unsafe_allow_html=True
        )

        if recommendations:
            total_jobs = len(recommendations)

            best_match = max(
                job["final_score"]
                for job in recommendations
            )

            average_match = sum(
                job["final_score"]
                for job in recommendations
            ) / total_jobs

            total_missing_skills = len(
                set(
                    skill
                    for job in recommendations
                    for skill in job["missing_skills"]
                )
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    " Jobs Found",
                    total_jobs
                )

            with col2:
                st.metric(
                    " Best Match",
                    f"{best_match:.2f}%"
                )

            with col3:
                st.metric(
                    " Average Match",
                    f"{average_match:.2f}%"
                )

            with col4:
                st.metric(
                    " Missing Skills",
                    total_missing_skills
                )
        # Job Match Comparison Chart
        st.markdown(
            '<div class="section-title">Job Match Comparison</div>',
            unsafe_allow_html=True
        )

        chart_data = pd.DataFrame({
            "Job": [
                job["job_title"]
                for job in recommendations
            ],
            "Match Score": [
                job["final_score"]
                for job in recommendations
            ]
        })

        st.bar_chart(
            chart_data.set_index("Job")
        )
        # --------------------------------------------------
        # Skill Overview
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Skill Overview</div>',
            unsafe_allow_html=True
        )

        all_matched_skills = set(
            skill
            for job in recommendations
            for skill in job["matched_skills"]
        )

        all_missing_skills = set(
            skill
            for job in recommendations
            for skill in job["missing_skills"]
        )

        skill_overview = pd.DataFrame({
            "Category": [
                "Skills You Have",
                "Skills To Learn"
            ],
            "Count": [
                len(all_matched_skills),
                len(all_missing_skills)
            ]
        })

        st.bar_chart(
            skill_overview.set_index("Category")
        )

        # --------------------------------------------------
        # Best Matching Job
        # --------------------------------------------------

        if recommendations:
            st.markdown(
                '<div class="section-title">Best Matching Job</div>',
                unsafe_allow_html=True
            )

            best_job = max(
                recommendations,
                key=lambda job: job["final_score"]
            )

            st.markdown(
                f"""
                <div class="job-card">
                    <div style="font-size: 24px; font-weight: 700; margin-bottom: 6px;">
                        {best_job["job_title"]}
                    </div>
                    <div style="font-size: 16px; margin-bottom: 15px;">
                        Personalized recommendation based on your resume and skills
                    </div>
                    <div style="font-size: 30px; font-weight: 700;">
                        {best_job["final_score"]:.2f}%
                    </div>
                    <div style="font-size: 14px;">
                        Overall Match
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Match Score",
                    f"{best_job['final_score']:.2f}%"
                )

            with col2:
                st.metric(
                    "Skills Matched",
                    len(best_job["matched_skills"])
                )

            with col3:
                st.metric(
                    "Skills Missing",
                    len(best_job["missing_skills"])
                )

        # --------------------------------------------------
        # Skill Distribution
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Skill Distribution</div>',
            unsafe_allow_html=True
        )

        skill_rows = []

        for job in recommendations:

            for skill in job["matched_skills"]:
                skill_rows.append({
                    "Skill": skill,
                    "Status": "Have"
                })

            for skill in job["missing_skills"]:
                skill_rows.append({
                    "Skill": skill,
                    "Status": "To Learn"
                })

        if skill_rows:

            skill_df = pd.DataFrame(skill_rows)

            skill_summary = (
                skill_df
                .groupby(["Skill", "Status"])
                .size()
                .reset_index(name="Job Count")
                .sort_values(
                    "Job Count",
                    ascending=False
                )
            )

            st.dataframe(
                skill_summary,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("No skill distribution data available.")

        # --------------------------------------------------
        # Download Recommendation Report
        # --------------------------------------------------

        st.markdown(
            '<div class="section-title">Download Recommendation Report</div>',
            unsafe_allow_html=True
        )

        report_data = []

        for job in recommendations:
            report_data.append({
                "Job Title": job["job_title"],
                "Overall Match (%)": job["final_score"],
                "Semantic Similarity (%)": job["semantic_score"],
                "Skill Match (%)": job["skill_score"],
                "Matched Skills": ", ".join(job["matched_skills"]),
                "Missing Skills": ", ".join(job["missing_skills"])
            })

        report_df = pd.DataFrame(report_data)

        csv_data = report_df.to_csv(index=False)

        st.download_button(
            label=" Download Job Recommendation Report",
            data=csv_data,
            file_name="job_recommendation_report.csv",
            mime="text/csv"
        )
        # --------------------------------------------------
        # PDF Recommendation Report
        # --------------------------------------------------

        st.write("###  Download PDF Report")

        pdf_file = "job_recommendation_report.pdf"

        generate_pdf_report(
            pdf_file,
            ats_score,
            skills,
            recommendations,
            suggestions
        )

        with open(pdf_file, "rb") as pdf:
            pdf_data = pdf.read()

        st.download_button(
            label=" Download PDF Recommendation Report",
            data=pdf_data,
            file_name="job_recommendation_report.pdf",
            mime="application/pdf"
        )

        st.subheader(
            " Top Job Recommendations"
        )

        if not recommendations:

            st.warning(
                "No jobs match your selected filters. "
                "Try lowering the minimum match percentage "
                "or changing the search criteria."
            )


        else:

            for i, job in enumerate(
                recommendations,
                start=1
            ):

                st.markdown(
                    f"### {i}. {job['job_title']}"
                )

                # --------------------------------------------------
                # Overall Match Score
                # --------------------------------------------------

                st.markdown(
                    "### Overall Match"
                )

                st.metric(
                    "Match Score",
                    f"{job['final_score']:.2f}%"
                )

                st.progress(
                    min(
                        job["final_score"] / 100,
                        1.0
                    )
                )

                # --------------------------------------------------
                # Semantic Similarity and Skill Match
                # --------------------------------------------------

                col1, col2 = st.columns(2)

                # Semantic Similarity

                with col1:

                    st.markdown(
                        "### Semantic Similarity"
                    )

                    st.metric(
                        "Score",
                        f"{job['semantic_score']:.2f}%"
                    )

                    st.progress(
                        min(
                            job["semantic_score"] / 100,
                            1.0
                        )
                    )

                # Skill Match

                with col2:

                    st.markdown(
                        "### Skill Match"
                    )

                    st.metric(
                        "Score",
                        f"{job['skill_score']:.2f}%"
                    )

                    st.progress(
                        min(
                            job["skill_score"] / 100,
                            1.0
                        )
                    )

                # --------------------------------------------------
                # Match Interpretation
                # --------------------------------------------------

                score = job["final_score"]

                if score >= 80:
                    st.success("Strong Match")

                elif score >= 60:
                    st.info("Good Match")

                elif score >= 40:
                    st.warning("Moderate Match")

                else:
                    st.error("Low Match")


                # --------------------------------------------------
                # Matching Skills
                # --------------------------------------------------

                st.markdown("**Matching Skills:**")


                if job["matched_skills"]:

                    st.write(
                        ", ".join(
                            job["matched_skills"]
                        )
                    )

                else:

                    st.write("None")


                # --------------------------------------------------
                # Missing Skills
                # --------------------------------------------------

                st.markdown("**Missing Skills:**")


                if job["missing_skills"]:

                    st.write(
                        ", ".join(
                            job["missing_skills"]
                        )
                    )

                else:

                    st.write("None")


                # --------------------------------------------------
                # Skill Gap Analysis
                # --------------------------------------------------

                st.markdown(
                    '<div class="section-title">Skill Gap Analysis</div>',
                    unsafe_allow_html=True
                )


                matched_skills = job[
                    "matched_skills"
                ]

                missing_skills = job[
                    "missing_skills"
                ]


                total_skills = (
                    len(matched_skills)
                    +
                    len(missing_skills)
                )


                if total_skills > 0:

                    skill_coverage = (
                        len(matched_skills)
                        /
                        total_skills
                    ) * 100

                else:

                    skill_coverage = 0


                st.write(
                    f"**Skill Coverage: "
                    f"{skill_coverage:.2f}%**"
                )


                st.progress(
                    min(
                        skill_coverage / 100,
                        1.0
                    )
                )

                # --------------------------------------------------
                # Skills User Has
                # --------------------------------------------------

                if matched_skills:

                    st.markdown(
                        '<div class="section-title">Skills You Have</div>',
                        unsafe_allow_html=True
                    )

                    for skill in matched_skills:
                        st.write(
                            skill
                        )

                # --------------------------------------------------
                # Skills User Should Learn
                # --------------------------------------------------

                if missing_skills:

                    st.markdown(
                        '<div class="section-title">Skills You Should Learn</div>',
                        unsafe_allow_html=True
                    )

                    for skill in missing_skills:
                        st.write(
                            skill
                        )

                else:

                    st.success(
                        "You have all the required "
                        "skills for this job!"
                    )

                st.divider()