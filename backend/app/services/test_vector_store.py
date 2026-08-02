from app.services.embedding_service import create_embedding
from app.services.vector_store import (
    add_document,
    search,
)

text = "FastAPI is a modern Python framework."

embedding = create_embedding(text)

add_document(
    doc_id="1",
    text=text,
    embedding=embedding,
)

results = search(
    create_embedding("Tell me about FastAPI")
)

print(results["documents"])