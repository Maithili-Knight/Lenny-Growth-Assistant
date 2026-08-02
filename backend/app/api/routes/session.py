from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from typing import List

from app.crud.session import create_session, get_all_sessions, update_session_title
from app.crud.message import get_session_messages
from app.schemas.session import SessionResponse, SessionUpdate
from app.schemas.message import MessageResponse

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post("/", response_model=SessionResponse)
def create_new_session(db: Session = Depends(get_db)):
    return create_session(db)


@router.get("/", response_model=List[SessionResponse])
def list_sessions(db: Session = Depends(get_db)):
    return get_all_sessions(db)


@router.get("/{session_id}/messages", response_model=List[MessageResponse])
def get_messages(session_id: int, db: Session = Depends(get_db)):
    return get_session_messages(db, session_id, limit=100)


@router.patch("/{session_id}", response_model=SessionResponse)
def rename_session(
    session_id: int,
    update: SessionUpdate,
    db: Session = Depends(get_db),
):
    session = update_session_title(db, session_id, update.title)
    if not session:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Session not found")
    return session