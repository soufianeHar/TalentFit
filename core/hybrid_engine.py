from scoring.matcher import compute_match_score
from semantic.similarity import compute_semantic_similarity


# Poids configurables
WEIGHTS = {
    "rule": 0.7,
    "semantic": 0.3
}


def compute_hybrid_score(cv_data, job_data):
    """
    Calcule le score hybride (rule-based + semantic).
    Retourne un dictionnaire structuré.
    """

    # ---- Rule-based score ----
    rule_result = compute_match_score(cv_data, job_data)
    rule_score = rule_result["final_score"]

    # Hard rejection prioritaire
    if rule_score == 0:
        return {
            "rule_score": 0,
            "semantic_score": 0,
            "hybrid_score": 0,
            "details": rule_result["details"]
        }

    # ---- Semantic similarity ----
    semantic_score = compute_semantic_similarity(
        cv_data["raw_text"],
        job_data["raw_text"]
    )

    # Mise à l’échelle sur 100
    semantic_scaled = semantic_score * 100

    # ---- Hybrid combination ----
    hybrid_score = (
        WEIGHTS["rule"] * rule_score
        + WEIGHTS["semantic"] * semantic_scaled
    )

    return {
        "rule_score": round(rule_score, 2),
        "semantic_score": round(semantic_score, 4),
        "hybrid_score": round(hybrid_score, 2),
        "details": rule_result["details"]
    }
