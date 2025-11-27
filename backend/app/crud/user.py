# backend/app/crud/user.py
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import CartItemSchema, CartSchema, ProductInCart, \
        UserCreate, UserUpdate, UserWithCartSchema
from typing import Optional

from app.models.cart import Cart, CartItem
from app.crud.base import AbstractCRUD


class UserCRUD(AbstractCRUD):
    """CRUD operations for User model."""

    async def get(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user_in: UserCreate) -> User:
        db_user = User(**user_in.model_dump())
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)  # опционально, чтобы были все поля
        return db_user

    async def update(self, db: AsyncSession, user_id: int,
                     user_update: UserUpdate) -> Optional[User]:
        db_user = await self.get_by_id(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)

        await db.flush()
        await db.refresh(db_user)
        return db_user

    async def delete(self, db: AsyncSession, user_id: int) -> bool:
        db_user = await self.get_by_id(db, user_id)
        if not db_user:
            return False
        await db.delete(db_user)
        await db.flush()
        return True

    async def get_users_with_carts(db: AsyncSession):
        result = await db.execute(
            select(User).options(
                selectinload(User.cart).selectinload(Cart.items)
                .selectinload(CartItem.product)
            )
        )
        return result.scalars().all()

    async def get_users_with_carts_dto(self, db: AsyncSession):
        users = await self.get_users_with_carts(db)
        return [
            UserWithCartSchema(
                id=u.id,
                firstName=u.firstName,
                lastName=u.lastName,
                email=u.email,
                cart=CartSchema(
                    items=[
                        CartItemSchema(
                            product=ProductInCart(
                                id=item.product.id,
                                title=item.product.title,
                                price=item.product.price
                            ),
                            quantity=item.quantity
                        )
                        for item in u.cart.items
                    ],
                    totalPrice=round(sum(item.quantity * item.product.price
                                         for item in u.cart.items), 2)
                ) if u.cart else None
            )
            for u in users
        ]
