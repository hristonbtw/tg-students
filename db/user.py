from sqlalchemy import Column, Integer, VARCHAR

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    # Telegram user id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    # Telegram user name
    username = Column(VARCHAR(32), unique=False, nullable=True)

    # Telegram user first name
    first_name = Column(VARCHAR(32), unique=False, nullable=False)

    # Telegram user second name
    second_name = Column(VARCHAR(32), unique=False, nullable=True)

    # User Role
    role = Column(VARCHAR(32), unique=False, nullable=False)

    def __str__(self) -> str:
        return f"<User:{self.user_id}>"
