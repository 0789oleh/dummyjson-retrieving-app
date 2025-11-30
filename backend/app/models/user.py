from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):
    __tablename__ = "users"
    first_name: Mapped[str] = mapped_column("firstName", String, index=True)
    last_name: Mapped[str] = mapped_column("lastName", String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
