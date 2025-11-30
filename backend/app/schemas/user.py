from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from app.schemas.cart import Cart


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    model_config = {"from_attributes": True}  # вместо class Config


class UserCreate(UserBase):
    pass


class ProductInCart(BaseModel):
    id: int
    title: str
    price: float
    model_config = {"from_attributes": True}


class CartItemSchema(BaseModel):
    product: ProductInCart
    quantity: int
    model_config = {"from_attributes": True}


class CartSchema(BaseModel):
    items: List[CartItemSchema]
    total_price: float
    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    model_config = {"from_attributes": True}


class User(UserBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}


class UserWithCartSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    cart: Optional[CartSchema] = None
    model_config = {"from_attributes": True}
