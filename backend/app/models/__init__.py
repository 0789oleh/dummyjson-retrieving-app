# backend/app/models/__init__.py
from .base import Base
from .user import User
from .product import Product      # ← добавь эту строку
from .cart import Cart, CartItem  # ← и эту


# Это заставит SQLAlchemy "увидеть" все таблицы
__all__ = ["Base", "User", "Product", "Cart", "CartItem"]
