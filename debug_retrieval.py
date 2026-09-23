from src.rag.document_loader import load_knowledge_base
from src.rag.chunker import chunk_documents
from src.rag.retriever import retrieve


# Load the knowledge base.
documents = load_knowledge_base("knowledge-base")

# Split documents into smaller chunks.
chunks = chunk_documents(documents)

# Test retrieval using a simplified search concept.
results = retrieve(
    "return window",
    chunks,
    top_k=5,
)

# Display the results.
print("\nTop retrieval results:\n")

for chunk, score in results:
    print(
        f"{score:.4f} | "
        f"{chunk.metadata.get('heading')} | "
        f"{chunk.document_filename}"
    )