from pathlib import Path

# Path to the cloned repository
DOCS_DIR = Path("../lennys-podcast-transcripts")


def load_documents():
    documents = []

    # Search recursively through all folders
    for file in DOCS_DIR.rglob("*.md"):
        text = file.read_text(encoding="utf-8")

        documents.append(
            {
                "filename": file.name,
                "path": str(file),
                "content": text,
            }
        )

    return documents