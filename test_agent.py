from src.rag.document_loader import load_knowledge_base
from src.rag.chunker import chunk_documents
from src.agent.agent import Agent


documents = load_knowledge_base(
    "knowledge-base"
)

chunks = chunk_documents(
    documents
)

agent = Agent(chunks)


print(
    agent.handle_message(
        "Can I return my backpack after 20 days?"
    )
)