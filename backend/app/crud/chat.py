from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.chat import ChatRequest
from app.services.ollama_service import generate_response


def chat(db: Session, request: ChatRequest):
    # Save user's message
    user_message = Message(
        session_id=request.session_id,
        role="user",
        content=request.prompt,
    )

    db.add(user_message)
    db.commit()

    # Generate AI response
    ai_response = generate_response(request.prompt)

    # Save AI message
    assistant_message = Message(
        session_id=request.session_id,
        role="assistant",
        content=ai_response,
    )

    db.add(assistant_message)
    db.commit()

    return {"response": ai_response}