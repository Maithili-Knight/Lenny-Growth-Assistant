from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest
from app.services.retriever import retrieve_context
from app.services.ollama_service import generate_rag_response

from app.crud.artifact import create_artifact
from app.schemas.artifact import ArtifactCreate
from app.services.ollama_service import generate_artifact

from app.crud.message import (
    create_message,
    get_session_messages,
)
from app.schemas.message import MessageCreate

def chat(
    db: Session,
    request: ChatRequest,
):
    # 1. Get previous messages (excluding the current user message)
    history_messages = get_session_messages(
        db=db,
        session_id=request.session_id,
        limit=10,
    )

    conversation_history = ""
    for message in history_messages:
        conversation_history += (
            f"{message.role.title()}: "
            f"{message.content}\n"
        )

    print("\n========== Conversation History ==========")
    print(conversation_history)
    print("==========================================\n")

    # 2. Save current user message
    create_message(
        db=db,
        session_id=request.session_id,
        message=MessageCreate(
            role="user",
            content=request.prompt,
        ),
    )

    # Retrieve relevant context
    chunks = retrieve_context(
        query=request.prompt,
        n_results=5,
    )

    context = "\n\n".join(chunks)

    # Generate AI response
    answer = generate_rag_response(
        question=request.prompt,
        context=context,
        history=conversation_history,
    )

    # Save assistant message
    create_message(
        db=db,
        session_id=request.session_id,
        message=MessageCreate(
            role="assistant",
            content=answer,
        ),
    )
    artifact_id = None

    artifact_keywords = [
        "summarize",
        "summary",
        "meeting notes",
        "action items",
        "todo",
        "to-do",
        "report",
        "blog",
        "notes",
    ]

    if any(keyword in request.prompt.lower() for keyword in artifact_keywords):
        artifact = generate_artifact(
            artifact_type="summary",
            prompt=request.prompt,
        )

        saved_artifact = create_artifact(
            db=db,
            artifact=ArtifactCreate(
                session_id=request.session_id,
                type=artifact["type"],
                title=artifact["title"],
                content=artifact["content"],
            ),
        )

        artifact_id = saved_artifact.id

    return {
        "response": answer,
        "artifact_id": artifact_id,
    }