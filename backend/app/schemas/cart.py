# backend/app/schemas/cart.py
from pydantic import BaseModel, PositiveInt, PositiveFloat
from typing import List, Optional
from datetime import datetime
from .product import Product  # импортируем полную схему продукта


class CartItemBase(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt = 1

    model_config = {"from_attributes": True}


class CartItemCreate(CartItemBase):
    pass


class CartItem(CartItemBase):
    id: int
    cart_id: int
    product: Product  # ← вложенный полный продукт (populate)

    model_config = {"from_attributes": True}


class CartBase(BaseModel):
    user_id: PositiveInt

    model_config = {"from_attributes": True}


class CartCreate(CartBase):
    items: List[CartItemCreate] = []  # фронт может прислать сразу товары


class CartUpdate(BaseModel):
    items: List[CartItemCreate] = []  # для PATCH — полностью заменяем состав


class Cart(CartBase):
    id: int
    created_at: Optional[datetime] = None

    # Дополнительные поля как в dummyjson (можно считать на лету)
    @property
    def total_quantity(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def total(self) -> float:
        return sum(item.quantity * item.product.price for item in self.items)

    @property
    def total_products(self) -> int:
        return len(self.items)

    @property
    def discounted_total(self) -> float:
        return self.total * 0.9  # например 10% скидка

    items: List[CartItem] = []  # ← тут будут полные товары с title/price

    model_config = {"from_attributes": True}
