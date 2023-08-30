from sqlalchemy import Column, Integer

from .base import BaseModel


class FullCourse(BaseModel):
    __tablename__ = "fullcourses"

    # Course id (from table Course)
    course = Column(Integer, unique=False, nullable=True)

    # Lesson id (from table Lessons)
    lesson = Column(Integer, unique=False, nullable=True)

    # Previous lesson (from table Lessons)
    previous_lesson = Column(Integer, unique=False, nullable=True)
