from src.rag.document_loader import load_knowledge_base
from src.rag.chunker import chunk_documents
from src.rag.retriever import retrieve

docs = load_knowledge_base("knowledge-base")
chunks = chunk_documents(docs)

results = retrieve(
    "How long does a TrailPlus member have to return an unused backpack?",
    chunks,
    top_k=5,
)

print("\n--- RESULTS ---")

for chunk, score in results:
    print("\n" + "=" * 60)
    print(f"SCORE: {score:.3f}")
    print(f"FILE: {chunk.document_filename}")
    print(f"HEADING: {chunk.metadata.get('heading')}")
    print(chunk.content)