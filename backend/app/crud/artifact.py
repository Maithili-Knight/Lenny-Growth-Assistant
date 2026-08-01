from sqlalchemy.orm import Session

from app.models.artifact import Artifact
from app.schemas.artifact import ArtifactCreate


def create_artifact(db: Session, artifact: ArtifactCreate):
    db_artifact = Artifact(
        session_id=artifact.session_id,
        type=artifact.type,
        title=artifact.title,
        content=artifact.content,
    )

    db.add(db_artifact)
    db.commit()
    db.refresh(db_artifact)

    return db_artifact


def get_artifact(db: Session, artifact_id: int):
    return (
        db.query(Artifact)
        .filter(Artifact.id == artifact_id)
        .first()
    )


def get_session_artifacts(db: Session, session_id: int):
    return (
        db.query(Artifact)
        .filter(Artifact.session_id == session_id)
        .all()
    )