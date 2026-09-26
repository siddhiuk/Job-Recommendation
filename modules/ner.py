import re
import spacy


# --------------------------------------------------
# Load spaCy English model
# --------------------------------------------------

nlp = spacy.load("en_core_web_sm")


# --------------------------------------------------
# Skill Dictionary
# Aligned with the 1200 Engineering Job Dataset
# --------------------------------------------------

SKILL_ALIASES = {

    "SQL": [
        "sql",
        "structured query language"
    ],

    "Python": [
        "python"
    ],

    "JavaScript": [
        "javascript",
        "java script",
        "js"
    ],

    "Cloud": [
        "cloud",
        "cloud computing",
        "cloud services"
    ],

    "Machine Learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "A/B Testing": [
        "a/b testing",
        "ab testing",
        "a-b testing",
        "a/b test"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy",
        "num py"
    ],

    "Git": [
        "git"
    ],

    "React": [
        "react",
        "reactjs",
        "react.js"
    ],

    "Data Visualization": [
        "data visualization",
        "data visualisation"
    ],

    "Excel": [
        "excel",
        "microsoft excel"
    ],

    "Statistics": [
        "statistics",
        "statistical analysis"
    ],

    "Testing": [
        "testing",
        "software testing",
        "unit testing",
        "integration testing"
    ],

    "APIs": [
        "api",
        "apis",
        "rest api",
        "rest apis",
        "api development"
    ],

    "Docker": [
        "docker"
    ],

    "ETL": [
        "etl",
        "extract transform load",
        "extract-transform-load"
    ],

    "Linux": [
        "linux",
        "ubuntu"
    ],


    # --------------------------------------------------
    # Additional common technical skills
    # --------------------------------------------------
    # These are useful for resume analysis even if they
    # are not currently present in the 1200-job dataset.

    "Java": [
        "java"
    ],

    "C++": [
        "c++"
    ],

    "C#": [
        "c#",
        "c sharp"
    ],

    "Artificial Intelligence": [
        "artificial intelligence",
        "ai"
    ],

    "Deep Learning": [
        "deep learning",
        "deep-learning"
    ],

    "Natural Language Processing": [
        "natural language processing",
        "nlp"
    ],

    "Computer Vision": [
        "computer vision"
    ],

    "Scikit-learn": [
        "scikit-learn",
        "scikit learn"
    ],

    "TensorFlow": [
        "tensorflow"
    ],

    "PyTorch": [
        "pytorch"
    ],

    "Matplotlib": [
        "matplotlib"
    ],

    "Django": [
        "django"
    ],

    "Flask": [
        "flask"
    ],

    "FastAPI": [
        "fastapi",
        "fast api"
    ],

    "Node.js": [
        "node.js",
        "nodejs",
        "node js"
    ],

    "TypeScript": [
        "typescript"
    ],

    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "css3"
    ],

    "MongoDB": [
        "mongodb",
        "mongo db"
    ],

    "MySQL": [
        "mysql"
    ],

    "PostgreSQL": [
        "postgresql",
        "postgres"
    ],

    "AWS": [
        "aws",
        "amazon web services"
    ],

    "Microsoft Azure": [
        "azure",
        "microsoft azure"
    ],

    "Google Cloud": [
        "google cloud",
        "gcp"
    ],

    "GitHub": [
        "github"
    ],

    "Generative AI": [
        "generative ai",
        "genai",
        "gen ai"
    ],

    "Agentic AI": [
        "agentic ai"
    ],

    "RAG": [
        "rag",
        "retrieval augmented generation",
        "retrieval-augmented generation"
    ]
}


# --------------------------------------------------
# Skill Extraction
# --------------------------------------------------

def extract_skills(text):

    if not text:
        return []

    text_lower = text.lower()

    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            pattern = re.escape(alias)

            pattern = (
                r"(?<!\w)"
                + pattern
                + r"(?!\w)"
            )

            if re.search(pattern, text_lower):

                found_skills.append(skill)

                break

    # Remove duplicates while preserving order
    return list(dict.fromkeys(found_skills))


# --------------------------------------------------
# Entity Extraction
# --------------------------------------------------

def extract_entities(text):

    if not text:
        return []

    # ----------------------------------------------
    # Step 1: Extract technical skills first
    # ----------------------------------------------

    skills = extract_skills(text)

    # ----------------------------------------------
    # Step 2: Run spaCy NER
    # ----------------------------------------------

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entity_text = ent.text.strip()

        # ------------------------------------------
        # Do not allow spaCy to classify a detected
        # technical skill as GPE / PERSON / ORG etc.
        # ------------------------------------------

        is_skill = False

        for skill in skills:

            aliases = SKILL_ALIASES.get(skill, [])

            if (
                    entity_text.lower() == skill.lower()
                    or entity_text.lower() in aliases
            ):
                is_skill = True
                break

        if not is_skill:

            entities.append({
                "text": entity_text,
                "label": ent.label_
            })

    # ----------------------------------------------
    # Step 3: Add detected technical skills as SKILL
    # ----------------------------------------------

    for skill in skills:

        entities.append({
            "text": skill,
            "label": "SKILL"
        })

    return entities