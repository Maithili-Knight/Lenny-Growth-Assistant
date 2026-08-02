from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate

from typing import List

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

from typing import List


def get_session_messages(
    db: Session,
    session_id: int,
    limit: int = 10,
) -> List[Message]:

    messages = (
        db.query(Message)
        .filter(Message.session_id == session_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    # Reverse to return in chronological order
    return messages[::-1]