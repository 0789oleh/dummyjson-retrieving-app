from itertools import count
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import join, select
from app.models.user import User
from app.models.cart import Cart, CartItem
from app.schemas.dashboard import UserWithCart
from app.models.product import Product


class DashboardCRUD:
    async def get_users_with_carts(self, db: AsyncSession,
                                   skip: int, limit: int):
        j = join(
            User,
            Cart,
            User.id == Cart.user_id,
            isouter=True
        ).join(
            CartItem,
            Cart.id == CartItem.cart_id,
            isouter=True
        ).join(
            Product,
            CartItem.product_id == Product.id,
            isouter=True
        )

        stmt = select(
            User.id,
            User.first_name,
            User.last_name,
            User.email,
            Cart.id.label("cart_id"),
            CartItem.id.label("item_id"),
            CartItem.quantity,
            Product.id.label("product_id"),
            Product.title,
            Product.price
        ).select_from(j).offset(skip).limit(limit)

        result = await db.execute(stmt)
        rows = result.all()
        # Дальше надо собрать структуру UserWithCart из строк
        users_dict = {}
        for row in rows:
            user_id = row.id
            if user_id not in users_dict:
                users_dict[user_id] = {
                    "id": row.id,
                    "first_name": row.first_name,
                    "last_name": row.last_name,
                    "email": row.email,
                    "cart": {
                        "id": row.cart_id,
                        "items": []
                    } if row.cart_id else None
                }
            if row.item_id:
                users_dict[user_id]["cart"]["items"].append({
                    "id": row.item_id,
                    "quantity": row.quantity,
                    "product": {
                        "id": row.product_id,
                        "title": row.title,
                        "price": row.price
                    }
                })

        return [UserWithCart.model_validate(u) for u in users_dict.values()]

    async def stats(self, db: AsyncSession):
        # Пример простой статистики: количество пользователей
        users = await db.execute(select(count(User)))
        count_users = users.scalar_one()
        return count_users
