import os
import re

KNOWN_SKILLS = [
    "python",
    "sql",
    "power bi",
    "excel",
    "tableau",
    "machine learning",
    "pandas",
    "numpy"
]

KNOWN_LANGUAGES = [
    "english",
    "french",
    "german",
    "spanish",
    "arabic"
]


def parse_cv(file_path):
    
    # Structure standard
    cv_data = {
        "skills": [],
        "years_experience": None,
        "languages": [],
        "tech_level": None
    }

    # Vérifier si le fichier existe
    if not os.path.exists(file_path):
        print("File does not exist.")
        return cv_data

    # Lire le contenu si c'est un fichier texte
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text_content = f.read()
    else:
        print("Unsupported file format.")
        return cv_data

    print("File successfully read.")

    text_content = text_content.lower()
    
    cv_data["raw_text"] = text_content

    extracted_skills = []

    for skill in KNOWN_SKILLS:
        if skill in text_content:
            extracted_skills.append(skill)

    cv_data["skills"] = extracted_skills

    experience_match = re.search(r"(\d+)\+?\s+years?", text_content)

    if experience_match:
        cv_data["years_experience"] = int(experience_match.group(1))
    
    extracted_languages = []

    for lang in KNOWN_LANGUAGES:
        if lang in text_content:
            extracted_languages.append(lang)

    cv_data["languages"] = extracted_languages

    years = cv_data["years_experience"]

    if years is not None:
        if years <= 1:
            cv_data["tech_level"] = "junior"
        elif 2 <= years <= 4:
            cv_data["tech_level"] = "intermediate"
        else:
            cv_data["tech_level"] = "senior"

    return cv_data
