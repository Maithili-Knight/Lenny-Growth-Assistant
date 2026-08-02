from tqdm import tqdm

from app.services.knowledge_loader import load_knowledge_base
from app.services.vector_store import (
    add_document,
    count_documents,
)


def build_vector_database():
    knowledge = load_knowledge_base()

    print(f"Knowledge chunks: {len(knowledge)}")

    if count_documents() > 0:
        print("Vector database already populated.")
        return

    for chunk in tqdm(knowledge):
        add_document(
            doc_id=chunk["id"],
            text=chunk["text"],
            embedding=chunk["embedding"],
        )

    print(f"\nIndexed {count_documents()} chunks.")