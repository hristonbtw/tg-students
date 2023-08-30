from sqlalchemy import Column, TEXT, VARCHAR

from .base import BaseModel


class Lesson(BaseModel):
    __tablename__ = "lessons"

    # Lesson title
    title = Column(VARCHAR(64), unique=False, nullable=False)

    # Lesson description
    description = Column(TEXT, uniqe=False, nullabe=True)

    # Lesson content
    content = Column(TEXT, uniqe=False, nullable=True)

    # Lesson task
    task = Column(TEXT, uniqe=False, nullable=True)
