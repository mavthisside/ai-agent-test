from src.rag.document_loader import load_knowledge_base


def test_load_knowledge_base():
    documents = load_knowledge_base("knowledge-base")

    assert len(documents) == 14


def test_returns_policy_metadata():
    documents = load_knowledge_base("knowledge-base")

    returns_policy = next(
        doc
        for doc in documents
        if doc.filename == "01-returns-policy-current.md"
    )

    assert returns_policy.metadata["status"] == "active"
    assert returns_policy.metadata["policy_authority"] == "official"
    assert returns_policy.metadata["document_id"] == "RET-2026-01"