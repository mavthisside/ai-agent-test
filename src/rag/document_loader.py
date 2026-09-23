from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    filename: str
    metadata: dict
    content: str


def load_document(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")

    # Split front matter from the actual document content.
    parts = text.split("---", 2)

    metadata = {}
    content = text

    if len(parts) == 3:
        front_matter = parts[1].strip()
        content = parts[2].strip()

        for line in front_matter.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

    return Document(
        filename=path.name,
        metadata=metadata,
        content=content,
    )


def load_knowledge_base(directory: str) -> list[Document]:
    path = Path(directory)

    documents = []

    for file in sorted(path.glob("*.md")):
        documents.append(load_document(file))

    return documents