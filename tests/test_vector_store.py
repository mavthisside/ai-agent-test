from src.rag.document_loader import load_knowledge_base
from src.rag.chunker import chunk_documents
from src.rag.vector_store import VectorStore


def test_vector_store_search():
    documents = load_knowledge_base("knowledge-base")
    chunks = chunk_documents(documents)

    store = VectorStore(chunks)

    results = store.search(
        "return policy",
        top_k=3,
    )

    assert len(results) == 3
    assert results[0][1] > 0