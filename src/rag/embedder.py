from sentence_transformers import SentenceTransformer


# This model runs entirely on our computer.
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str) -> list[float]:
    embedding = model.encode(text)

    return embedding.tolist()