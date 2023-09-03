from sqlalchemy import Column, TEXT, VARCHAR, LargeBinary, SmallInteger

from .base import BaseModel


class Lesson(BaseModel):
    __tablename__ = "lessons"

    # Lesson id
    id = Column(SmallInteger, unique=True, nullable=False, primary_key=True)

    # Lesson title
    title = Column(VARCHAR(64), unique=True, nullable=False)

    # Lesson description
    description = Column(TEXT, unique=False, nullable=False)

    # Lesson content
    content = Column(TEXT, unique=False, nullable=False)

    # Lesson task
    task = Column(LargeBinary, unique=False, nullable=False)

    # Lesson task filename
    task_filename = Column(TEXT, unique=False, nullable=False)

    def __str__(self) -> str:
        return f"<Lesson:{self.title}>"
