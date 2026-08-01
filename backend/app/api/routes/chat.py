from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.chat import chat
from app.database.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat_with_ai(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    return chat(db, request)