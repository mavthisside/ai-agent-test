from dataclasses import dataclass

from src.rag.document_loader import Document


@dataclass
class Chunk:
    chunk_id: str
    document_filename: str
    metadata: dict
    content: str


def chunk_document(document: Document) -> list[Chunk]:
    lines = document.content.splitlines()

    chunks = []
    current_heading = None
    current_lines = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Treat Markdown headings as section boundaries.
        if line.startswith("#"):
            if current_lines:
                chunks.append(
                    create_chunk(
                        document,
                        current_heading,
                        current_lines,
                        len(chunks),
                    )
                )

            current_heading = line.lstrip("#").strip()
            current_lines = []

        else:
            current_lines.append(line)

    # Add the final section.
    if current_lines:
        chunks.append(
            create_chunk(
                document,
                current_heading,
                current_lines,
                len(chunks),
            )
        )

    return chunks


def create_chunk(
    document: Document,
    heading: str | None,
    lines: list[str],
    index: int,
) -> Chunk:

    content = "\n".join(lines)

    if heading:
        content = f"{heading}\n\n{content}"

    return Chunk(
        chunk_id=f"{document.filename}:{index}",
        document_filename=document.filename,
        metadata={
            **document.metadata,
            "heading": heading,
        },
        content=content,
    )


def chunk_documents(documents: list[Document]) -> list[Chunk]:
    chunks = []

    for document in documents:
        chunks.extend(chunk_document(document))

    return chunks