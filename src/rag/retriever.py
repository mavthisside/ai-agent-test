import re

from src.rag.chunker import Chunk
from src.rag.query import build_search_query
from src.rag.vector_store import VectorStore


def is_retrievable(chunk: Chunk) -> bool:
    status = chunk.metadata.get("status", "").lower()
    audience = chunk.metadata.get("audience", "").lower()
    authority = chunk.metadata.get("policy_authority", "").lower()

    if status in {"superseded", "draft"}:
        return False

    if audience == "internal":
        return False

    if authority != "official":
        return False

    return True


def tokenize(text: str) -> set[str]:
    return set(
        re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
    )


def heading_relevance(
    query: str,
    heading: str | None,
) -> float:

    if not heading:
        return 0.0

    query_words = tokenize(query)
    heading_words = tokenize(heading)

    if not query_words or not heading_words:
        return 0.0

    overlap = query_words & heading_words

    return len(overlap) / len(query_words)


def retrieve(
    query: str,
    chunks: list[Chunk],
    top_k: int = 3,
    membership_tier: str | None = None,
    vector_store: VectorStore | None = None,
) -> list[tuple[Chunk, float]]:

    # Understand the user's query first.
    search_info = build_search_query(
        query,
        membership_tier=membership_tier,
    )

    # Build the vector store once if one wasn't supplied.
    if vector_store is None:
        eligible_chunks = [
            chunk
            for chunk in chunks
            if is_retrievable(chunk)
        ]

        vector_store = VectorStore(eligible_chunks)

    # Search using the stored embeddings.
    vector_results = vector_store.search(
        search_info.search_query,
        top_k=len(vector_store.chunks),
    )

    scored_chunks = []

    for chunk, semantic_score in vector_results:

        if not is_retrievable(chunk):
            continue

        heading_score = heading_relevance(
            search_info.search_query,
            chunk.metadata.get("heading"),
        )

        final_score = (
            semantic_score * 0.75
            + heading_score * 0.25
        )

        scored_chunks.append(
            (chunk, final_score)
        )

    print("\nRETRIEVAL SCORES:")
    for chunk, score in scored_chunks:
        print(score, chunk.metadata.get("heading"))

    scored_chunks.append(
    (chunk, final_score)
        )

    scored_chunks.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    MIN_RELEVANCE_SCORE = 0.40

    return [
        item
        for item in scored_chunks[:top_k]
        if item[1] >= MIN_RELEVANCE_SCORE
    ]