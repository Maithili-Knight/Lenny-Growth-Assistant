from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: int
    prompt: str


class ChatResponse(BaseModel):
    response: str
    artifact_id: Optional[int] = None