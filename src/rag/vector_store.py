import numpy as np

from src.rag.chunker import Chunk
from src.rag.embedder import create_embedding


class VectorStore:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks

        # Create embeddings once when the store is built.
        self.embeddings = np.array(
            [
                create_embedding(chunk.content)
                for chunk in chunks
            ]
        )

    def search(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[tuple[Chunk, float]]:

        query_embedding = np.array(
            create_embedding(query)
        )

        # Calculate cosine similarity against all stored embeddings.
        similarities = (
            self.embeddings @ query_embedding
            / (
                np.linalg.norm(self.embeddings, axis=1)
                * np.linalg.norm(query_embedding)
            )
        )

        # Highest similarity first.
        ranked_indices = np.argsort(
            similarities
        )[::-1]

        results = []

        for index in ranked_indices[:top_k]:
            results.append(
                (
                    self.chunks[index],
                    float(similarities[index]),
                )
            )

        return results