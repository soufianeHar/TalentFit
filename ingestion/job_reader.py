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

def parse_job(file_path):

    job_data = {
        "required_skills": [],
        "min_experience": None,
        "required_languages": [],
        "required_level": None
    }

    with open(file_path, "r", encoding="utf-8") as f:
        text_content = f.read().lower()

    for skill in KNOWN_SKILLS:
        if skill in text_content:
            job_data["required_skills"].append(skill)
    
        experience_match = re.search(r"(\d+)\+?\s+years?", text_content)

    if experience_match:
        job_data["min_experience"] = int(experience_match.group(1))

    for lang in KNOWN_LANGUAGES:

        if lang in text_content:
            job_data["required_languages"].append(lang)

        if "junior" in text_content:
            job_data["required_level"] = "junior"
        elif "intermediate" in text_content:
            job_data["required_level"] = "intermediate"
        elif "senior" in text_content:
            job_data["required_level"] = "senior"

    return job_data
