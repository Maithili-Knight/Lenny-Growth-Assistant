from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    SQLAlchemy Declarative Base class.
    All models inherit from this base to register with SQLAlchemy's metadata.
    """
    pass