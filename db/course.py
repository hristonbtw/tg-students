from sqlalchemy import Column, Integer, VARCHAR, TEXT, Boolean

from .base import BaseModel


class Course(BaseModel):
    __tablename__ = "courses"

    # Course name
    title = Column(VARCHAR(64), unique=False, nullable=False, primary_key=True)

    # Course description
    description = Column(TEXT, unique=False, nullable=True)

    # Course active status
    is_active = Column(Boolean, default=True)

    # Course lifetime
    lifetime = Column(Integer, unique=False, nullable=True)

    def __str__(self) -> str:
        return f'<Course:{self.title}>'
