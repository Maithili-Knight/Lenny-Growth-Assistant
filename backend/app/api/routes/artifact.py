from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.artifact import (
    create_artifact,
    get_artifact,
    get_session_artifacts,
)
from app.database.session import get_db
from app.schemas.artifact import (
    ArtifactCreate,
    ArtifactResponse,
)

router = APIRouter(
    prefix="/artifacts",
    tags=["Artifacts"],
)


@router.post(
    "/",
    response_model=ArtifactResponse,
)
def create(
    artifact: ArtifactCreate,
    db: Session = Depends(get_db),
):
    return create_artifact(db, artifact)


@router.get(
    "/{artifact_id}",
    response_model=ArtifactResponse,
)
def get(
    artifact_id: int,
    db: Session = Depends(get_db),
):
    return get_artifact(db, artifact_id)


@router.get(
    "/session/{session_id}",
    response_model=List[ArtifactResponse],
)
def get_all(
    session_id: int,
    db: Session = Depends(get_db),
):
    return get_session_artifacts(db, session_id)