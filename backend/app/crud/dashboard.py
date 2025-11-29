from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.schemas.user import User
from app.schemas.cart import Cart, CartItem
from app.schemas.dashboard import UserWithCart


class DashboardCRUD:
    '''This class handles dashboard-related database operations.
    Does not implement create/update/delete.'''
    async def get_users_with_carts(self, db: AsyncSession, skip: int,
                                   limit: int) -> List[UserWithCart]:
        # Один запрос с JOIN'ами
        result = await db.execute(
            select(User)
            .options(joinedload(User.carts).joinedload(Cart.items)
                     .joinedload(CartItem.product))
            .offset(skip)
            .limit(limit)
        )
        users = result.scalars().unique().all()

        return [UserWithCart.from_orm(user) for user in users]
