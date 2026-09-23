from src.rag.document_loader import load_knowledge_base
from src.rag.chunker import chunk_documents
from src.rag.retriever import retrieve


def test_retrieve_standard_return_policy():
    documents = load_knowledge_base("knowledge-base")
    chunks = chunk_documents(documents)

    results = retrieve(
        "Can I return an item after 20 days?",
        chunks,
        top_k=3,
        membership_tier="standard",
    )

    assert len(results) == 3

    top_chunk, score = results[0]

    assert "30 calendar days" in top_chunk.content
    assert score > 0


def test_retrieve_does_not_return_superseded_policy():
    documents = load_knowledge_base("knowledge-base")
    chunks = chunk_documents(documents)

    results = retrieve(
        "What is the return window?",
        chunks,
        top_k=5,
        membership_tier="standard",
    )

    for chunk, score in results:
        assert chunk.metadata.get("status") != "superseded"