from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models import Application, Car, Client, User, Role
from sqlalchemy.orm import selectinload

from app.schemas.requests import ApplyAppAdminRequest, RejectAppAdminRequest, ApplyTimeAdminRequest
from app.schemas.responses import DiagNamesList, AdminGetFinishAppResponse,AppListItem, AdminGetStartAppResponse
router = APIRouter()

async def find_app(app_id: int,session: AsyncSession):
    app = await session.scalar(select(Application).where(Application.id == app_id))
    if app is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.get(
    "/get_app/{app_id}",
    status_code=status.HTTP_200_OK,
    response_model=AdminGetStartAppResponse,
)
async def start_app(
        app_id: int,
        session: AsyncSession = Depends(deps.get_session)):
    app = await find_app(app_id, session)
    if not app:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    result_car = await session.execute(select(Car).where(Car.id == app.car_id))
    car = result_car.scalars().first()
    if not car:
        raise HTTPException(status_code=404, detail="Машина не найдена")
    result_client = await session.execute(select(Client).where(Client.client_id == app.client_id))
    client = result_client.scalars().first()
    if not client:
        raise HTTPException(status_code=404, detail="клиент не найден")
    return AdminGetStartAppResponse(
        app_id = app.id,
        client_id = app.client_id,
        car_id = app.car_id,
        problem = app.problem,
        conn = app.conn,
        phone = client.phone,
        brand = car.brand,
        model = car.model,
        number = car.number,
        year = car.year
    )

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

@router.get(
    "/get_all_apps",
    status_code=status.HTTP_200_OK,
    response_model=list[AppListItem]
)
async def get_all_apps(
    client_id: int | None = None,
    car_id: str | None = None,
    session: AsyncSession = Depends(deps.get_session)
):
    query = (
        select(Application)
        .options(selectinload(Application.car),
        selectinload(Application.client))
        .order_by(Application.created_at.desc())
    )
    if client_id:
        query = query.where(Application.client_id == client_id)
    if car_id:
        query = query.where(Car.number.ilike(f"%{car_id}%"))
    result = await session.execute(query)
    apps = result.scalars().all()
    if not apps:
        raise HTTPException(status_code=404, detail="Не найдено")
    return [AppListItem.model_validate(app) for app in apps]

@router.get(
    "/diagnostics",
    status_code=status.HTTP_200_OK,
    response_model=list[DiagNamesList]
)
async def get_diagnostics(
        session: AsyncSession = Depends(deps.get_session
)):
    result = await session.execute(
        select(User.user_id, User.user_name)
        .where(User.role == Role.DIAGNOSTIC)
    )
    rows = result.mappings().all()

    return rows