from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    session_id: Optional[int] = None
    prompt: Optional[str] = None
    llm_provider: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    artifact_id: Optional[int] = None