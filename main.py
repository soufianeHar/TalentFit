from ingestion.cv_reader import parse_cv
from ingestion.job_reader import parse_job
from scoring.matcher import compute_match_score

if __name__ == "__main__":
    result = parse_cv("data/cvs/test.txt")
    print(result)

job = parse_job("data/cvs/job.txt")

print(job)

score = compute_match_score(result,job)

print("Matching score :",score)