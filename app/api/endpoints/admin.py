from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models import Application

from app.schemas.requests import ApplyAppAdminRequest, RejectAppAdminRequest, ApplyTimeAdminRequest
from app.schemas.responses import AdminGetFinishAppResponse
router = APIRouter()

async def find_app(app_id: int,session: AsyncSession):
    app = await session.scalar(select(Application).where(Application.id == app_id))
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.post(
    "/adminapply",
    status_code=status.HTTP_200_OK,
    response_model=ApplyAppAdminRequest
)
async def adminapply_app(
    app_id: int,
    apply_data: ApplyAppAdminRequest,
    session: AsyncSession = Depends(deps.get_session)
):
    app = await find_app(app_id, session)

    app.admin_comment = apply_data.admin_comment
    app.status = apply_data.status
    app.priority = apply_data.priority
    app.diag_id = apply_data.diag_id

    await session.commit()
    await session.refresh(app)

    return app

@router.post(
    "/adminreject",
    status_code=status.HTTP_200_OK,
    response_model=RejectAppAdminRequest
)
async def adminreject_app(
        app_id: int,
        reject_data: RejectAppAdminRequest,
        session: AsyncSession = Depends(deps.get_session)
):
    app = await find_app(app_id, session)

    app.admin_comment = reject_data.admin_comment
    app.status = reject_data.status

    await session.commit()
    await session.refresh(app)
    return app

@router.post(
    "/adminapplytime",
    status_code=status.HTTP_200_OK,
    response_model=ApplyTimeAdminRequest)
async def adminapply_time(
        app_id: int,
        arrival_time: datetime,
        session: AsyncSession = Depends(deps.get_session)
):
    app = await find_app(app_id, session)
    app.arrival_time = arrival_time
    await session.commit()
    await session.refresh(app)
    return app

@router.post(
    "/admingetfinishapp",
    status_code=status.HTTP_200_OK,
    response_model=AdminGetFinishAppResponse
)
async def adminget_finish_app(
        app_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    app = await find_app(app_id, session)
