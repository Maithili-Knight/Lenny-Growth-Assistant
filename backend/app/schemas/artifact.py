from pydantic import BaseModel


class ArtifactCreate(BaseModel):
    session_id: int
    type: str
    title: str
    content: str


class ArtifactResponse(ArtifactCreate):
    id: int

    class Config:
        from_attributes = True