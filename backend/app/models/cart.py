# backend/app/models/cart.py
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

# ← ЭТО ОБЯЗАТЕЛЬНО — импортируем SQLAlchemy-модель!
from app.models.product import Product

from .base import Base


class Cart(Base):
    __tablename__ = "carts"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    items: Mapped[List["CartItem"]] = relationship(
        "CartItem", back_populates="cart", cascade="all, delete-orphan"
    )


class CartItem(Base):
    __tablename__ = "cart_items"

    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped[Product] = relationship(Product)
