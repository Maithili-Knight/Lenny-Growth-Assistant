from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud.message import create_message
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter(
    prefix="/sessions",
    tags=["Messages"],
)


@router.post(
    "/{session_id}/messages",
    response_model=MessageResponse,
)
def create_new_message(
    session_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
):
    return create_message(
        db,
        session_id,
        message,
    )