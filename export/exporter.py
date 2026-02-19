import csv


def export_results_to_csv(ranked_results, filename="results.csv"):
    """
    ranked_results: liste [(cv_name, result_dict)]
    """

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Header
        writer.writerow([
            "cv_name",
            "rule_score",
            "semantic_score",
            "hybrid_score"
        ])

        # Rows
        for cv_name, result in ranked_results:
            writer.writerow([
                cv_name,
                result["rule_score"],
                result["semantic_score"],
                result["hybrid_score"]
            ])

    print(f"\nResults exported to {filename}")
