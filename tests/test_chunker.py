from src.rag.document_loader import load_knowledge_base
from src.rag.chunker import chunk_documents


def test_chunk_knowledge_base():
    documents = load_knowledge_base("knowledge-base")
    chunks = chunk_documents(documents)

    assert len(chunks) > len(documents)


def test_returns_policy_chunk_contains_return_window():
    documents = load_knowledge_base("knowledge-base")
    chunks = chunk_documents(documents)

    return_chunk = next(
        chunk
        for chunk in chunks
        if "30 calendar days" in chunk.content
    )

    assert return_chunk.metadata["status"] == "active"
    assert return_chunk.metadata["policy_authority"] == "official"