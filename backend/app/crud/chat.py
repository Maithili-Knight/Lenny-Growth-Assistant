from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest
from app.models.message import Message
from app.services.retriever import retrieve_context
from app.services.ollama_service import generate_rag_response


def chat(db: Session, request: ChatRequest):
    # 1. Save user message to PostgreSQL database
    db_user_message = Message(
        session_id=request.session_id,
        role="user",
        content=request.prompt,
    )
    db.add(db_user_message)
    db.commit()

    # 2. Retrieve relevant chunks from ChromaDB
    chunks = retrieve_context(
        query=request.prompt,
        n_results=5,
    )

    # Validate that retrieve_context() returns valid chunks (list of strings)
    if not isinstance(chunks, list):
        raise ValueError("retrieve_context() did not return a list of chunks.")

    # 3. Print retrieved chunks before sending them to Ollama (Requirement 5)
    print("\n================ RETRIEVED CHUNKS ================\n")
    for i, chunk in enumerate(chunks, start=1):
        print(f"--- Chunk {i} ---")
        print(chunk)
        print("-" * 50)
    print("\n===================================================\n")

    # Combine retrieved chunks into a single context
    context = "\n\n".join(chunks)

    # Validate that generate_rag_response() receives valid context (Requirement 6)
    if not context.strip():
        context = "[System Message: No relevant documents were found in the knowledge base.]"

    # 4. Generate answer using Ollama RAG
    answer = generate_rag_response(
        question=request.prompt,
        context=context,
    )

    # 5. Save assistant response to PostgreSQL database
    db_assistant_message = Message(
        session_id=request.session_id,
        role="assistant",
        content=answer,
    )
    db.add(db_assistant_message)
    db.commit()
    db.refresh(db_assistant_message)

    return {
        "response": answer
    }