from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import logging

from app.database.session import get_db
from app.crud.chat import (
    chat,
    chat_stream,
)
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.services.llm_service import generate_llm_response

logger = logging.getLogger(__name__)

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
    # 1. Router-level empty check (returns 400)
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Invalid input: 'message' field is required and cannot be empty."
        )
        
    try:
        # 2. Call CRUD chat handler (handles RAG, DB storage, and artifacts)
        return chat(
            db=db,
            request=request,
        )
        
    except ValueError as ve:
        # Caught validation error (e.g. Unsupported LLM provider or empty message)
        logger.error(f"Validation error in chat endpoint: {str(ve)}")
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )
    except RuntimeError as re:
        # Caught connection error (e.g. Ollama service unavailable, Claude API key missing/billing error)
        logger.error(f"Runtime error in chat endpoint: {str(re)}")
        raise HTTPException(
            status_code=500,
            detail=str(re)
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post("/stream")
def chat_stream_endpoint(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    return StreamingResponse(
        chat_stream(db, request),
        media_type="text/plain",
    )