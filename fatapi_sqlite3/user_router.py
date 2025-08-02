
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db_models import User, get_db
from schemas import UserCreateUpdatePydantic

from fastapi import APIRouter, Depends, HTTPException, status
user_router = APIRouter()


@user_router.get("/users")
async def fetch_users(db:AsyncSession = Depends(get_db)):
    users = await db.execute(select(User))
    users = users.scalars().all()
    return { 'users': users }

@user_router.post("/register")
async def create_user(user_data: UserCreateUpdatePydantic, db:AsyncSession = Depends(get_db)):
    existing_user = await db.execute(select(User).where(User.username == user_data.username))
    if existing_user.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")
    
    new_user = User(username=user_data.username, email=user_data.email)
    try:
        async with db.begin():
            db.add(new_user)
        await db.commit()
        await db.refresh(new_user)  # Refresh to get the updated user with generated id

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    # users = await db.execute(select(User))
    # users = users.scalars().all()
    return { 'data': new_user }