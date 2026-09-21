# 💼 Job Recommendation System

An AI-powered **Job Recommendation System** that analyzes a user's resume and recommends relevant job opportunities based on **resume matching, semantic similarity, and Named Entity Recognition (NER)**.

The system extracts important information from a resume, compares it with available job descriptions, calculates similarity scores, and recommends jobs that best match the candidate's skills and experience.

## 🚀 Features

- 📄 **Resume Upload**
  - Upload a resume in PDF format.
  - Extracts text automatically from the uploaded resume.

- 🔍 **Resume Matching**
  - Compares resume content with available job descriptions.
  - Identifies relevant skills and qualifications.

- 🧠 **Semantic Similarity**
  - Uses Natural Language Processing to understand the meaning of resume and job-description text.
  - Calculates similarity between the candidate's resume and job descriptions.

- 🏷️ **Named Entity Recognition (NER)**
  - Extracts important entities and information from resume text.
  - Helps identify skills, technologies, organizations, qualifications, and other relevant information.

- 💼 **Job Recommendation**
  - Ranks available jobs according to their relevance to the candidate's profile.
  - Provides suitable job recommendations based on matching scores.

- 🌐 **Interactive Web Interface**
  - Built using Streamlit.
  - Simple interface for uploading resumes and viewing recommendations.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Pandas | Data processing |
| Scikit-learn | Machine learning and similarity calculations |
| NLP | Resume and job-description analysis |
| NER | Entity extraction |
| PyMuPDF | PDF text extraction |

## 📂 Project Structure

```text
Job-Recommendation/
│
├── app.py
├── jobs.csv
├── requirements.txt
├── README.md
├── .gitignore
│
└── modules/
    ├── __init__.py
    ├── resume_parser.py
    ├── resume_matching.py
    ├── semantic_similarity.py
    ├── ner.py
    └── recommender.py
```

## 🔄 How It Works

```text
                ┌─────────────────┐
                │   Upload Resume │
                └────────┬────────┘
                         ↓
                ┌─────────────────┐
                │ Resume Parsing  │
                └────────┬────────┘
                         ↓
              ┌──────────────────────┐
              │ Extract Resume Text  │
              └──────────┬───────────┘
                         ↓
             ┌────────────────────────┐
             │ NLP & NER Processing   │
             └────────────┬───────────┘
                          ↓
             ┌────────────────────────┐
             │ Semantic Similarity    │
             │ & Resume Matching      │
             └────────────┬───────────┘
                          ↓
             ┌────────────────────────┐
             │ Compare with Job Data  │
             └────────────┬───────────┘
                          ↓
             ┌────────────────────────┐
             │ Rank Matching Jobs      │
             └────────────┬───────────┘
                          ↓
             ┌────────────────────────┐
             │ Job Recommendations    │
             └────────────────────────┘
```

## 📊 Dataset

The project uses a CSV dataset containing job information such as:

- Job title
- Job description
- Required skills
- Qualifications
- Other relevant job information

The dataset can be extended with additional job listings to improve the range of recommendations.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/siddhiuk/Job-Recommendation.git
```

### 2. Navigate to the project

```bash
cd Job-Recommendation
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

The application will be available locally at:

```text
http://localhost:8501
```

## 🌐 Live Demo

The application can be deployed using **Streamlit Community Cloud**.

**Live Demo:**  
_Add your Streamlit deployment URL here after deployment._

## 🎯 Project Objectives

The main objectives of this project are to:

1. Automate the initial resume-job matching process.
2. Reduce the time required to search for relevant jobs.
3. Use NLP techniques to understand resume and job-description content.
4. Identify important skills and entities from resumes.
5. Recommend jobs based on relevance rather than simple keyword matching.
6. Provide an easy-to-use interface for candidates.

## 🔮 Future Enhancements

- 🔹 Integration with real-time job portals and APIs
- 🔹 Personalized career recommendations
- 🔹 Skill-gap analysis
- 🔹 Resume improvement suggestions
- 🔹 ATS compatibility score
- 🔹 Multiple resume formats
- 🔹 Advanced transformer-based semantic similarity
- 🔹 User profile and recommendation history
- 🔹 Location-based job recommendations
- 🔹 Personalized learning and course recommendations

## 👩‍💻 Project Skills Demonstrated

This project demonstrates practical knowledge of:

- Python
- Machine Learning
- Natural Language Processing
- Semantic Similarity
- Named Entity Recognition
- Data Processing
- Recommendation Systems
- Streamlit
- Git & GitHub
- Web Application Development

## 📌 Use Case

This system can help **students, fresh graduates, and job seekers** quickly identify job opportunities that are relevant to their skills and resume.

Instead of manually checking every job description, the system automatically analyzes the candidate's resume and ranks relevant job opportunities.

## 📄 License

This project is developed for educational and academic purposes.
