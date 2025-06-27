from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models import Application

from app.schemas.responses import DiagGetAppResponse
from app.schemas.requests import DiagFinishRequest
router = APIRouter()

async def find_app(app_id: int,session: AsyncSession):
    app = await session.scalar(select(Application).where(Application.id == app_id))
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.get(
    "/get_app",
    status_code=status.HTTP_200_OK,
    response_model=DiagGetAppResponse
)
async def get_app(
        app_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    app = await find_app(app_id, session)
    return app

@router.post(
    "/diag_finish",
    status_code=status.HTTP_200_OK,
    response_model=DiagFinishRequest
)
async def diag_finish(
        app_id: int,
        diag_apply_data: DiagFinishRequest,
        session: AsyncSession = Depends(deps.get_session)):
    app = await find_app(app_id, session)

    app.diag_comment=diag_apply_data.diag_comment
    app.diag_price=diag_apply_data.diag_price

    await session.commit()
    await session.refresh(app)
    return app
    