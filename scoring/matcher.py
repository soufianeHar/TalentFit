def compute_match_score(cv_data, job_data):

    total_score = 0
    details = {}

    must_have = job_data.get("must_have_skills", [])
    nice_to_have = job_data.get("nice_to_have_skills", [])

    matched_must = [s for s in must_have if s in cv_data["skills"]]
    missing_must = [s for s in must_have if s not in cv_data["skills"]]

    if must_have and len(matched_must) == 0:
        return {
            "final_score": 0,
            "details": {"reason": "No must-have skills matched"}
        }

    skills_score = 0

    if must_have:
        skills_score += (len(matched_must) / len(must_have)) * 40

    matched_nice = [s for s in nice_to_have if s in cv_data["skills"]]
    if nice_to_have:
        skills_score += (len(matched_nice) / len(nice_to_have)) * 10
    penalty = 0

    if len(missing_must) > 0:
        penalty = 10  # penalty for missing must-have

    total_score += skills_score
    total_score -= penalty

    details["matched_must"] = matched_must
    details["missing_must"] = missing_must
    details["matched_nice"] = matched_nice
    details["penalty"] = penalty
    details["skills_score"] = round(skills_score, 2)


    # ---- Languages ----
    required_languages = job_data["required_languages"]
    matched_languages = [
        lang for lang in required_languages
        if lang in cv_data["languages"]
    ]

    if required_languages:
        lang_score = (len(matched_languages) / len(required_languages)) * 20
    else:
        lang_score = 0

    total_score += lang_score
    details["language_score"] = round(lang_score, 2)
    details["matched_languages"] = matched_languages

    # ---- Experience ----
    exp_score = 0
    exp_gap = None

    if job_data["min_experience"] is not None and cv_data["years_experience"] is not None:
        min_exp = job_data["min_experience"]
        cv_exp = cv_data["years_experience"]
        exp_gap = cv_exp - min_exp

        if cv_exp >= min_exp:
            exp_score = 20
        else:
            exp_score = (cv_exp / min_exp) * 20

    total_score += exp_score
    details["experience_score"] = round(exp_score, 2)
    details["experience_gap"] = exp_gap

    # ---- Tech level ----
    level_score = 0
    level_gap = None
    level_map = {"junior": 1, "intermediate": 2, "senior": 3}

    cv_level = cv_data["tech_level"]
    job_level = job_data["required_level"]

    if cv_level and job_level:
        level_gap = level_map[cv_level] - level_map[job_level]

        if level_gap >= 0:
            level_score = 10
        elif level_gap == -1:
            level_score = 5

    total_score += level_score
    details["level_score"] = level_score
    details["level_gap"] = level_gap

    return {
        "final_score": round(total_score, 2),
        "details": details
    }

