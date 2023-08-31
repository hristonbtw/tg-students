from sqlalchemy import Column, TEXT, VARCHAR

from .base import BaseModel


class Lesson(BaseModel):
    __tablename__ = "lessons"

    # Lesson title
    title = Column(VARCHAR(64), unique=False, nullable=False, primary_key=True)

    # Lesson description
    description = Column(TEXT, unique=False, nullable=True)

    # Lesson content
    content = Column(TEXT, unique=False, nullable=True)

    # Lesson task
    task = Column(TEXT, unique=False, nullable=True)

    def __str__(self) -> str:
        return f"<Lesson:{self.title}>"
