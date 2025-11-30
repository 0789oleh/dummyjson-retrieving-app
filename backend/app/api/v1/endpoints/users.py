from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate, UserWithCartSchema
from app.database import get_db
from app.crud.base import AbstractCRUD
from app.crud.user import UserCRUD

router = APIRouter(prefix="/users", tags=["users"])
userCRUD: UserCRUD = AbstractCRUD.create_crud(UserCRUD)


@router.get("", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100,
                     db: AsyncSession = Depends(get_db)):
    users = await userCRUD.get(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int,
                    db: AsyncSession = Depends(get_db)):
    db_user = await userCRUD.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("", response_model=User,
             status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate,
                      db: AsyncSession = Depends(get_db)):
    return await userCRUD.create(db, user_in)


@router.patch("/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate,
                      db: AsyncSession = Depends(get_db)):
    db_user = await userCRUD.update(db, user_id, user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      db: AsyncSession = Depends(get_db)):
    success = await userCRUD.delete(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None


@router.get("/with-carts", response_model=List[UserWithCartSchema])
async def get_users_with_carts(db: AsyncSession = Depends(get_db)):
    return await userCRUD.get_users_with_carts_dto(db)
