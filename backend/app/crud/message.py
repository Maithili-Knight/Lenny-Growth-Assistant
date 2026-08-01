from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate


def create_message(
    db: Session,
    session_id: int,
    message: MessageCreate,
) -> Message:

    db_message = Message(
        session_id=session_id,
        role=message.role,
        content=message.content,
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message