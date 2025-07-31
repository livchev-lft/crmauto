from datetime import datetime
from fastapi.responses import Response

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, bindparam, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api import deps
from app.models import Client, Car, Application, ACTIVE_STATUSES
from app.schemas.requests import AppRegisterRequest, ClientRegisterRequest, CarRegisterRequest
from app.schemas.responses import CheckClient, GetAppsResponse, CheckCarResponse

router = APIRouter()

@router.get(
    "/check_client",
    status_code=status.HTTP_200_OK,
    response_model=CheckClient)
async def check_client(
        client_id: int,
        session: AsyncSession = Depends(deps.get_session)):
    stmt = select(Client).where(Client.client_id == bindparam("client_id", type_=BigInteger))
    client = await session.scalar(stmt.params(client_id=client_id))
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
async def my_car(
        client_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    result = await session.execute(select(Car).where(Car.client_id == client_id, Car.is_deleted == False))
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
        client_id = app_data.client_id,
        car_id = app_data.car_id,
        problem = app_data.problem,
        conn = app_data.conn,
        created_at = datetime.now()
    )
    session.add(new_app)
    await session.commit()
    return {"id": new_app.id}

@router.delete("/delete_car/{car_id}")
async def delete_car(
        car_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    result = await session.execute(select(Car).where(Car.id == car_id))
    car = result.scalar_one_or_none()
    if not car:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    car.is_deleted = True
    session.add(car)
    await session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/replace_phone")
async def replace_phone(
        client_id: int,
        phone: str,
        session: AsyncSession = Depends(deps.get_session)
):
    result = await session.execute(select(Client).where(Client.client_id == client_id))
    client = result.scalars().first()
    if not client:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    client.phone = phone
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/get_apps",
            response_model=list[GetAppsResponse],
            status_code=status.HTTP_200_OK
            )
async def get_apps(
        client_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    result = await session.execute(select(Application).where(Application.client_id == client_id))
    apps = result.scalars().all()
    return apps

@router.get("/check_car_app")
async def get_app_car(
        car_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    stmt = select(Application).where(
        Application.car_id == car_id,
        Application.status.in_(ACTIVE_STATUSES)
    )
    result = await session.execute(stmt)
    app = result.scalars().first()
    if app:
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/check_client_car",
            response_model=CheckCarResponse,
            status_code=status.HTTP_200_OK
            )
async def check_client_car(
        car_id: int,
        session: AsyncSession = Depends(deps.get_session)
):
    result = await session.execute(select(Car).where(Car.id == car_id))
    car = result.scalars().first()
    return car