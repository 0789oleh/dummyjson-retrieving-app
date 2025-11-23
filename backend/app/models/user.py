from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from typing import Optional


class User(Base):
    __tablename__ = "users"
    firstName: Mapped[str] = mapped_column(String, index=True)
    lastName: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    # Добавь другие поля из dummyjson, если нужно
