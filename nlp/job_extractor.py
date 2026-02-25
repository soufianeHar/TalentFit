import re

# petite taxonomie / synonymes (MVP)
SYNONYMS = {
    "powerbi": "power bi",
    "ml": "machine learning",
    "bi": "business intelligence",
    "python3": "python",
    "postgres": "postgresql",
}

LEVEL_KEYWORDS = {
    "junior": ["junior", "entry", "beginner"],
    "intermediate": ["intermediate", "mid", "confirmed"],
    "senior": ["senior", "expert", "lead"],
}

LANGUAGES = ["english", "french", "arabic", "german", "spanish"]

def normalize_token(token: str) -> str:
    t = token.strip().lower()
    t = re.sub(r"\s+", " ", t)
    t = t.replace("-", " ")
    t = SYNONYMS.get(t, t)
    return t

def extract_years_experience(text: str):
    """
    Ex: '2 years', '3+ years', 'minimum 1 year'
    """
    text = text.lower()

    patterns = [
        r"(\d+)\s*\+\s*years",
        r"(\d+)\s*\+\s*year",
        r"(\d+)\s*years",
        r"(\d+)\s*year",
        r"minimum\s*(\d+)\s*years",
        r"at least\s*(\d+)\s*years",
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return int(m.group(1))
    return None

def extract_level(text: str):
    t = text.lower()
    for level, kws in LEVEL_KEYWORDS.items():
        if any(kw in t for kw in kws):
            return level
    return None

def extract_languages(text: str):
    t = text.lower()
    found = []
    for lang in LANGUAGES:
        if lang in t:
            found.append(lang)
    return found

def extract_skills_from_text(text: str, skill_bank: list):
    """
    skill_bank = liste de compétences possibles (ex: python, sql, power bi...)
    """
    t = normalize_token(text)
    matched = []

    # matching par présence simple (MVP)
    for skill in skill_bank:
        s = normalize_token(skill)
        if s in t:
            matched.append(s)

    # uniq
    return sorted(list(set(matched)))

def build_job_data(raw_text: str, skill_bank: list):

    raw_text_norm = raw_text.lower()

    years = extract_years_experience(raw_text_norm)
    level = extract_level(raw_text_norm)
    langs = extract_languages(raw_text_norm)

    # séparation par sections simples
    must_section = ""
    nice_section = ""

    if "nice to have" in raw_text_norm:
        parts = raw_text_norm.split("nice to have")
        must_section = parts[0]
        nice_section = parts[1]
    elif "preferred" in raw_text_norm:
        parts = raw_text_norm.split("preferred")
        must_section = parts[0]
        nice_section = parts[1]
    else:
        must_section = raw_text_norm

    must_skills = extract_skills_from_text(must_section, skill_bank)
    nice_skills = extract_skills_from_text(nice_section, skill_bank)

    job_data = {
        "required_skills": must_skills,
        "nice_to_have_skills": nice_skills,
        "min_experience": years,
        "required_level": level,
        "required_languages": langs,
        "raw_text": raw_text_norm
    }

    return job_data