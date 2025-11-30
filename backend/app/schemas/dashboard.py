from typing import Optional
from typing import List
from app.schemas.product import Product
from pydantic import BaseModel, field_validator


class CartItemWithProduct(BaseModel):
    id: int
    quantity: int
    product: Product


class CartWithItems(BaseModel):
    id: int
    total: float
    items: List[CartItemWithProduct]

    @field_validator('total', mode='before')
    def calculate_total(cls, v, values):
        if 'items' in values and values['items']:
            return sum(item.product.price * item.quantity
                       for item in values['items'])
        return v


class UserWithCart(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    cart: Optional[CartWithItems] = None

    model_config = {"from_attributes": True, "populate_by_name": True}
