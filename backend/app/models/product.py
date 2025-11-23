# backend/app/models/cart.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Product(Base):
    __tablename__ = "products"
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[int] = mapped_column()
