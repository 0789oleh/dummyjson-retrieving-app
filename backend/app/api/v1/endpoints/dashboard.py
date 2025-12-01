from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.dashboard import UserWithCart
from app.crud.dashboard import DashboardCRUD

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
dashboardCRUD: DashboardCRUD = DashboardCRUD()


@router.get("/users-with-carts", response_model=List[UserWithCart])
async def get_users_with_carts(skip: int = 0, limit: int = 100,
                               db: AsyncSession = Depends(get_db)):
    return await dashboardCRUD.get_users_with_carts(db, skip, limit)


@router.get("/stats", response_model=List[UserWithCart])
async def get_stats(skip: int = 0, limit: int = 100,
                           db: AsyncSession = Depends(get_db)):
    return await dashboardCRUD.stats(db, skip, limit)
