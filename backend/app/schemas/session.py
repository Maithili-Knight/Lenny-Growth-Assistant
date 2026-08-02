from datetime import datetime

from pydantic import BaseModel


class SessionCreate(BaseModel):
    """
    Data received from the frontend
    when creating a new chat.

    For now, the frontend sends nothing.
    """
    pass


class SessionUpdate(BaseModel):
    """
    Data received from the frontend
    when renaming a chat session.
    """
    title: str


class SessionResponse(BaseModel):
    """
    Data returned to the frontend.
    """

    id: int
    title: str
    llm_provider: str
    created_at: datetime

    class Config:
        from_attributes = True