from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models import Application

from app.schemas.responses import MechanicGetResponse
from app.schemas.requests import MechanicFinishRequest

router = APIRouter()

async def find_app(app_id: int,session: AsyncSession):
    app = await session.scalar(select(Application).where(Application.id == app_id))
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.get(
    "/mechanic_getapp",
    status_code=status.HTTP_200_OK,
    response_model=MechanicGetResponse
)
async def mechanic_get_app(
        app_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    app = await find_app(app_id, session)
    return app

@router.post(
    "/mechanic_finish_app",
    status_code=status.HTTP_200_OK,
    response_model=MechanicFinishRequest
)
async def mechanic_finish_app(
        app_id: int,
        mechanic_data: MechanicFinishRequest,
        session: AsyncSession = Depends(deps.get_session)
):
    app = await find_app(app_id, session)

    app.mechanic_comment = mechanic_data.mechanic_comment
    app.mechanic_price = mechanic_data.mechanic_price

    await session.commit()
    await session.refresh(app)
    return app