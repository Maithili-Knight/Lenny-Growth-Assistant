from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging
import traceback

from app.crud.chat import chat
from app.database.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

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
    try:
        return chat(db, request)
    except Exception as e:
        error_msg = f"Error in chat endpoint: {str(e)}"
        logger.error(f"{error_msg}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=error_msg,
        )