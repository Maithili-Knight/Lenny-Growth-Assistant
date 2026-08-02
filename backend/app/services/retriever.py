from app.services.embedding_service import create_embedding
from app.services.vector_store import search, count_documents
import logging

logger = logging.getLogger(__name__)


def retrieve_context(
    query: str,
    n_results: int = 5,
):
    if not query or not query.strip():
        logger.warning("Empty query received in retrieve_context")
        return []

    # Validate that ChromaDB contains documents
    total_docs = count_documents()
    if total_docs == 0:
        logger.error("ChromaDB vector store is empty! No documents found to retrieve context from.")
        raise ValueError("ChromaDB vector store is empty. Please populate the database.")

    query_embedding = create_embedding(query)

    results = search(
        query_embedding=query_embedding,
        n_results=n_results,
    )

    if not results or "documents" not in results or not results["documents"]:
        logger.warning(f"No results returned from ChromaDB for query: {query}")
        return []

    documents = results["documents"][0]
    return documents if documents is not None else []