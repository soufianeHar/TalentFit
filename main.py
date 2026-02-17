from ingestion.cv_reader import parse_cv

if __name__ == "__main__":
    result = parse_cv("data/cvs/test.txt")
    print(result)
