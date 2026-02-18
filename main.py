import os
from ingestion.cv_reader import parse_cv
from ingestion.job_reader import parse_job
from scoring.matcher import compute_match_score

cv_folder = "data/cvs"
cv_results = []

for filename in os.listdir(cv_folder):
    if filename.endswith(".txt") and filename != "job.txt":

        path = os.path.join(cv_folder, filename)

        cv_data = parse_cv(path)
        
        cv_results.append((filename, cv_data))

scored_cvs = []

job = parse_job("data/cvs/job.txt")

for filename, cv_data in cv_results:
    result = compute_match_score(cv_data,job)
    scored_cvs.append((filename, result))

scored_cvs.sort(key=lambda x: x[1]["final_score"], reverse=True)

# scored_cvs = [item for item in scored_cvs if item[1] > 0]

for filename, result in scored_cvs:
    print("\n", filename)
    print("Score:", result["final_score"])
    print("Details:", result["details"])
