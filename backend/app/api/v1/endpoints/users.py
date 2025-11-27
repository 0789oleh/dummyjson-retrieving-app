from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud import user as crud_user
from app.schemas.user import User, UserCreate, UserUpdate, UserWithCartSchema
from app.database import get_db
from app.crud.base import AbstractCRUD
from app.crud.user import UserCRUD


class UserController:
    """Controller for User endpoints."""

    __router = APIRouter(prefix="/users", tags=["users"])
    __userCRUD: UserCRUD = AbstractCRUD.create_crud()

    @__router.get("/", response_model=List[User])
    async def read_users(self, skip: int = 0, limit: int = 100,
                         db: AsyncSession = Depends(get_db)):
        users = await self.__userCRUD.get(db, skip=skip, limit=limit)
        return users

    @__router.get("/{user_id}", response_model=User)
    async def read_user(self, user_id: int,
                        db: AsyncSession = Depends(get_db)):
        db_user = await self.__userCRUD.get_by_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    @__router.post("/", response_model=User,
                   status_code=status.HTTP_201_CREATED)
    async def create_user(self, user_in: UserCreate,
                          db: AsyncSession = Depends(get_db)):
        return await self.__userCRUD.create(db, user_in)

    @__router.patch("/{user_id}", response_model=User)
    async def update_user(self, user_id: int, user_update: UserUpdate,
                          db: AsyncSession = Depends(get_db)):
        db_user = await self.__userCRUD.update(db, user_id, user_update)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user

    @__router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_user(self, user_id: int,
                          db: AsyncSession = Depends(get_db)):
        success = await self.__userCRUD.delete(db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return None

    @__router.get("/with-carts", response_model=List[UserWithCartSchema])
    async def get_users_with_carts(self, db: AsyncSession = Depends(get_db)):
        return await crud_user.get_users_with_carts_dto(db)

    def get_router(self):
        return self.__router
