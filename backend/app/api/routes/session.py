from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.crud.session import create_session
from app.schemas.session import SessionResponse

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post("/", response_model=SessionResponse)
def create_new_session(db: Session = Depends(get_db)):
    return create_session(db)