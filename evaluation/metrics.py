def precision_at_k(ranked_results, ground_truth, k):
    """
    ranked_results: liste triée [(filename, result_dict)]
    ground_truth: dict {"cv_name": 1 ou 0}
    k: top-k à évaluer
    """

    top_k = ranked_results[:k]

    relevant_count = 0

    for filename, _ in top_k:
        if ground_truth.get(filename, 0) == 1:
            relevant_count += 1

    return relevant_count / k

def recall_at_k(ranked_results, ground_truth, k):
    """
    ranked_results: liste triée [(filename, result_dict)]
    ground_truth: dict {"cv_name": 1 ou 0}
    k: top-k à évaluer
    """

    top_k = ranked_results[:k]

    # Nombre total de candidats pertinents dans le dataset
    total_relevant = sum(ground_truth.values())

    if total_relevant == 0:
        return 0

    relevant_in_top_k = 0

    for filename, _ in top_k:
        if ground_truth.get(filename, 0) == 1:
            relevant_in_top_k += 1

    return relevant_in_top_k / total_relevant
