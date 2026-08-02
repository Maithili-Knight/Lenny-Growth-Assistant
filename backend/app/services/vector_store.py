import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="knowledge_base"
)


def add_document(doc_id, text, embedding):
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding],
    )


def search(query_embedding, n_results=5):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )


def count_documents():
    return collection.count()