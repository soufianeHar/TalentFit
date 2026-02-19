from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Charger le modèle une seule fois
model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_semantic_similarity(cv_text, job_text):
    """
    Retourne un score de similarité entre 0 et 1
    """

    embeddings = model.encode([cv_text, job_text])
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return round(float(similarity), 4)
