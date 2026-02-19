import os
from ingestion.cv_reader import parse_cv
from ingestion.job_reader import parse_job
from core.hybrid_engine import compute_hybrid_score
from evaluation.metrics import precision_at_k, recall_at_k
from export.exporter import export_results_to_csv

cv_folder = "data/cvs"
cv_results = []

# ---- Load CVs ----
for filename in os.listdir(cv_folder):
    if filename.endswith(".txt") and filename != "job.txt":
        path = os.path.join(cv_folder, filename)
        cv_data = parse_cv(path)
        cv_results.append((filename, cv_data))

# ---- Load Job ----
job = parse_job("data/cvs/job.txt")

# ---- Compute hybrid scores ----
ranked_results = []

for filename, cv_data in cv_results:
    result = compute_hybrid_score(cv_data, job)
    ranked_results.append((filename, result))

# ---- Sort by hybrid score ----
ranked_results.sort(
    key=lambda x: x[1]["hybrid_score"],
    reverse=True
)

# ---- Display results ----
for filename, result in ranked_results:
    print("\n--------------------------")
    print("CV:", filename)
    print("Rule score:", result["rule_score"])
    print("Semantic score:", result["semantic_score"])
    print("Hybrid score:", result["hybrid_score"])
    print("Details:", result["details"])
print("\n===== Evaluation =====")

# ---- Ground truth (golden set) ----
# 1 = relevant
# 0 = not relevant

GROUND_TRUTH = {
    "cv1.txt": 1,
    "cv2.txt": 1,
    "cv3.txt": 0
}
print("\n===== Evaluation =====")

for k in [1, 2, 3]:
    p_at_k = precision_at_k(ranked_results, GROUND_TRUTH, k)
    r_at_k = recall_at_k(ranked_results, GROUND_TRUTH, k)

    print(f"Precision@{k}: {round(p_at_k, 2)}")
    print(f"Recall@{k}: {round(r_at_k, 2)}\n")

# ---- Export CSV ----
export_results_to_csv(ranked_results)
