from sqlalchemy.orm import Session

from app.models.session import ChatSession


def create_session(db: Session) -> ChatSession:
    """
    Create a new chat session.
    """

    session = ChatSession()

    db.add(session)
    db.commit()
    db.refresh(session)

    return session