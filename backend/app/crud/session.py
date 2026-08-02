from sqlalchemy.orm import Session

from app.models.session import ChatSession


from typing import List

def create_session(db: Session) -> ChatSession:
    """
    Create a new chat session.
    """

    session = ChatSession()

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_all_sessions(db: Session) -> List[ChatSession]:
    """
    List all chat sessions.
    """
    return db.query(ChatSession).order_by(ChatSession.created_at.desc()).all()


def update_session_title(db: Session, session_id: int, title: str) -> ChatSession:
    """
    Update a chat session's title.
    """
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        return None
    session.title = title
    db.commit()
    db.refresh(session)
    return session