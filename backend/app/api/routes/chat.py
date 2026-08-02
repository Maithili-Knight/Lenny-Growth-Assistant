from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.crud.chat import chat

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    return chat(
        db=db,
        request=request,
    )