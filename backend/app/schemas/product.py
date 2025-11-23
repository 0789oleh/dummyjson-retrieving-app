# backend/app/schemas/product.py — УДАЛЯЕМ ProductCreate полностью
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    title: str
    description: str | None = None  # ← nullable!
    price: float

    model_config = {"from_attributes": True}


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

    model_config = {"from_attributes": True}


class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class Product(ProductBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
