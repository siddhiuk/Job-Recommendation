import streamlit as st
import pandas as pd

from modules.resume_parser import extract_text
from modules.ner import extract_skills, extract_entities
from modules.recommender import recommend_jobs


st.set_page_config(
    page_title="AI Job Recommendation System",
    page_icon="💼",
    layout="wide"
)


st.title("💼 AI-Based Job Recommendation System")

st.write(
    "Upload your resume and get personalized job recommendations "
    "using NER, resume matching and semantic similarity."
)


jobs = pd.read_csv("jobs.csv")


uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf"]
)


if uploaded_file:

    st.success("Resume uploaded successfully!")

    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")

    st.text_area(
        "Extracted Resume Text",
        resume_text,
        height=200
    )


    # NER / Skills

    skills = extract_skills(resume_text)

    st.subheader("🧠 Skills Detected")

    if skills:

        st.write(", ".join(skills))

    else:

        st.warning(
            "No predefined technical skills detected."
        )


    # General NER

    entities = extract_entities(resume_text)

    st.subheader("🔍 Named Entities")

    if entities:

        for entity in entities:

            st.write(
                f"**{entity['text']}** → {entity['label']}"
            )


    # Recommendation

    if st.button("🚀 Find Best Jobs"):

        with st.spinner(
            "Analyzing resume and matching jobs..."
        ):

            recommendations = recommend_jobs(
                resume_text,
                skills,
                jobs
            )


        st.subheader(
            "🏆 Top Job Recommendations"
        )


        for i, job in enumerate(
            recommendations,
            start=1
        ):

            st.markdown(
                f"### {i}. {job['job_title']}"
            )

            st.metric(
                "Overall Match",
                f"{job['final_score']}%"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Semantic Similarity:** "
                    f"{job['semantic_score']}%"
                )

                st.write(
                    f"**Skill Match:** "
                    f"{job['skill_score']}%"
                )


            with col2:

                st.write("**✅ Matching Skills**")

                if job["matched_skills"]:

                    st.write(
                        ", ".join(
                            job["matched_skills"]
                        )
                    )

                else:

                    st.write("None")


                st.write("**❌ Missing Skills**")

                if job["missing_skills"]:

                    st.write(
                        ", ".join(
                            job["missing_skills"]
                        )
                    )

                else:

                    st.write("None")

            st.divider()