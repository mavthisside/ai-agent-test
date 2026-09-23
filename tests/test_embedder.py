from src.rag.embedder import create_embedding


def test_create_embedding():
    embedding = create_embedding(
        "Customers can return an item within 30 days."
    )

    assert isinstance(embedding, list)
    assert len(embedding) > 0