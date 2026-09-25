import re
import spacy


# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


# --------------------------------------------------
# Skill Dictionary
# --------------------------------------------------

SKILL_ALIASES = {

    "Python": [
        "python"
    ],

    "Java": [
        "java"
    ],

    "C": [
        "c programming",
        "c language"
    ],

    "C++": [
        "c++"
    ],

    "C#": [
        "c#",
        "c sharp"
    ],

    "SQL": [
        "sql",
        "structured query language"
    ],

    "Machine Learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "Deep Learning": [
        "deep learning",
        "deep-learning"
    ],

    "Artificial Intelligence": [
        "artificial intelligence",
        "ai"
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

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    "Matplotlib": [
        "matplotlib"
    ],

    "Flask": [
        "flask"
    ],

    "Django": [
        "django"
    ],

    "FastAPI": [
        "fastapi",
        "fast api"
    ],

    "React": [
        "react",
        "reactjs",
        "react.js"
    ],

    "JavaScript": [
        "javascript",
        "js"
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

    "Bootstrap": [
        "bootstrap"
    ],

    "Node.js": [
        "node.js",
        "nodejs",
        "node js"
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

    "Docker": [
        "docker"
    ],

    "Kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "Linux": [
        "linux"
    ],

    "Git": [
        "git"
    ],

    "GitHub": [
        "github"
    ],

    "Networking": [
        "networking",
        "computer networking"
    ],

    "Cyber Security": [
        "cyber security",
        "cybersecurity",
        "cyber-security"
    ],

    "Cryptography": [
        "cryptography"
    ],

    "SIEM": [
        "siem"
    ],

    "Power BI": [
        "power bi",
        "powerbi"
    ],

    "Excel": [
        "excel",
        "microsoft excel"
    ],

    "Tableau": [
        "tableau"
    ],

    "Transformers": [
        "transformers",
        "transformer models"
    ],

    "Generative AI": [
        "generative ai",
        "genai",
        "gen ai"
    ],

    "Agentic AI": [
        "agentic ai"
    ]
}


# --------------------------------------------------
# Entity Extraction
# --------------------------------------------------

def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:

        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities


# --------------------------------------------------
# Skill Extraction
# --------------------------------------------------

def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            # Escape special characters such as + and .
            pattern = re.escape(alias)

            # Word-boundary matching
            pattern = r"(?<!\w)" + pattern + r"(?!\w)"

            if re.search(pattern, text):

                found_skills.append(skill)

                break

    # Remove duplicates while preserving order
    return list(dict.fromkeys(found_skills))