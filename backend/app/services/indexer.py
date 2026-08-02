from app.services.loader import load_documents
from app.services.chunker import chunk_text
from app.services.embedding_service import create_embedding
from app.services.vector_store import add_document


def build_index():
    documents = load_documents()

    chunk_count = 0

    for doc in documents:
        chunks = chunk_text(doc["content"])

        for i, chunk in enumerate(chunks):
            embedding = create_embedding(chunk)

            add_document(
                doc_id=f"{doc['filename']}_{i}",
                text=chunk,
                embedding=embedding,
            )

            chunk_count += 1

    print(f"Indexed {chunk_count} chunks.")