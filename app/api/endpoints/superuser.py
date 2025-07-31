from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models import User
from app.schemas.requests import AddUserRequest

router = APIRouter()

@router.post("/add_user",
             status_code=status.HTTP_201_CREATED,
             response_model=AddUserRequest)
async def add_user(
        user_data: AddUserRequest,
        session: AsyncSession = Depends(deps.get_session),
):
    existing_user = await session.scalar(select(User).where(User.user_id == user_data.user_id))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )
    new_user = User(
        user_id=user_data.user_id,
        role=user_data.role,
        user_name=user_data.user_name,
        hashed_password=user_data.hashed_password,
        phone=user_data.phone
    )
    session.add(new_user)
    await session.commit()
    return new_user
