from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps

from app.schemas.responses import CheckClient, CheckCarResponse
from app.schemas.requests import AppRegisterRequest, ClientRegisterRequest, CarRegisterRequest
from app.models import Client, Car, Application

router = APIRouter()

@router.get(
    "/check_client",
    status_code=status.HTTP_200_OK,
    response_model=CheckClient)
async def check_client(
        client_id: int,
        session: AsyncSession = Depends(deps.get_session)):
    client = await session.scalar(select(Client).where(Client.client_id == client_id))
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client {client_id} not found"
        )
    return client

@router.post(
    "/register_client",
    status_code=status.HTTP_201_CREATED)
async def register_client(
        client_data: ClientRegisterRequest,
        session: AsyncSession = Depends(deps.get_session)
):
    new_client = Client(
        client_id=client_data.client_id,
        user_name=client_data.user_name,
        phone=client_data.phone
    )
    session.add(new_client)
    await session.commit()
    print("гуд")
    return {"detail": "Success"}

@router.get(
    "/mycars/{client_id}",
    response_model=list[CheckCarResponse],
    status_code=status.HTTP_200_OK
)
async def mycar(
        client_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    result = await session.execute(select(Car).where(Car.client_id == client_id))
    cars = result.scalars().all()
    return cars

@router.post("/addcar")
async def add_car(
        car_data: CarRegisterRequest,
        session: AsyncSession = Depends(deps.get_session)
):
    new_car = Car(
        client_id=car_data.client_id,
        brand=car_data.brand,
        model=car_data.model,
        number=car_data.number,
        year=car_data.year
    )
    session.add(new_car)
    await session.commit()
    return {"detail": "Success"}

@router.post("/addapp")
async def add_app(
        app_data: AppRegisterRequest,
        session: AsyncSession = Depends(deps.get_session)
):
    new_app = Application(
        client_id=app_data.client_id,
        car_id=app_data.car_id,
        problem = app_data.problem,
        created_at = datetime.now()
    )
    session.add(new_app)
    await session.commit()
    return {"detail": "Success"}

