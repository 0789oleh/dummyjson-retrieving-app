from typing import Optional
from pydantic import BaseModel


class UserWithCart(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    cart: Optional[CartWithItems] = None
    
    class Config:
        from_attributes = True


class CartWithItems(BaseModel):
    id: int
    total: float
    items: List[CartItemWithProduct]
    
    @validator('total', pre=True)
    def calculate_total(cls, v, values):
        if 'items' in values and values['items']:
            return sum(item.product.price * item.quantity for item in values['items'])
        return v


class CartItemWithProduct(BaseModel):
    id: int
    quantity: int
    product: Product
