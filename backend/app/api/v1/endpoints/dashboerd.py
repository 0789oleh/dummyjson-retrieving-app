from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.dashboard import UserWithCart
from app.crud.dashboard import DashboardCRUD


class DashboardController:
    __router = APIRouter(prefix="/dashboard", tags=["dashboard"])
    __dashboardCRUD: DashboardCRUD = DashboardCRUD()

    @__router.get("/users-with-carts", response_model=List[UserWithCart])
    async def get_users_with_carts(
        self,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
    ):
        return await self.__dashboardCRUD.get_users_with_carts(db, skip, limit)

    def get_router(self):
        return self.__router
