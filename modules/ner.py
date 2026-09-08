import spacy

nlp = spacy.load("en_core_web_sm")


SKILLS = [
    "python",
    "java",
    "sql",
    "machine learning",
    "deep learning",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "flask",
    "django",
    "react",
    "javascript",
    "html",
    "css",
    "aws",
    "docker",
    "kubernetes",
    "linux",
    "networking",
    "cyber security",
    "siem",
    "nlp",
    "transformers",
    "power bi",
    "excel",
    "git"
]


def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return entities


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill.title())

    return list(set(found_skills))