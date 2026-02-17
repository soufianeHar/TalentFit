def compute_match_score(cv_data, job_data):

    score = 0

    # ---- Skills (50 pts) ----
    required_skills = job_data["required_skills"]
    matched_skills = [
        skill for skill in required_skills
        if skill in cv_data["skills"]
    ]

    if required_skills:
        skills_score = (len(matched_skills) / len(required_skills)) * 50
        score += skills_score

    # ---- Languages (20 pts) ----
    required_languages = job_data["required_languages"]
    matched_languages = [
        lang for lang in required_languages
        if lang in cv_data["languages"]
    ]

    if required_languages:
        lang_score = (len(matched_languages) / len(required_languages)) * 20
        score += lang_score

    # ---- Experience (20 pts) ----
    if job_data["min_experience"] is not None and cv_data["years_experience"] is not None:
        min_exp = job_data["min_experience"]
        cv_exp = cv_data["years_experience"]

        if cv_exp >= min_exp:
            score += 20
        else:
            score += (cv_exp / min_exp) * 20

    # ---- Tech level (10 pts) ----
    level_map = {"junior": 1, "intermediate": 2, "senior": 3}

    cv_level = cv_data["tech_level"]
    job_level = job_data["required_level"]

    if cv_level and job_level:
        diff = level_map[cv_level] - level_map[job_level]

        if diff >= 0:
            score += 10
        elif diff == -1:
            score += 5

    return round(score, 2)
