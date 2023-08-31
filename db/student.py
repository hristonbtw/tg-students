from sqlalchemy import Column, Integer, Boolean, DateTime

from .base import BaseModel


class Student(BaseModel):
    __tablename__ = "students"

    # Student user_id (From table User)
    user_id = Column(Integer, nullable=False, unique=True, primary_key=True)

    # Student course (From table FromCourse)
    course = Column(Integer, nullable=False, unique=False)

    # Student payment status
    payment = Column(Boolean, default=False)

    # Student start time
    start_data = Column(DateTime, nullable=True, unique=False)

    # Student active lesson (From table Lesson)
    active_lesson = Column(Integer, nullable=True, unique=False)

    def __str__(self) -> str:
        return f'<Student:{self.user_id}>'
