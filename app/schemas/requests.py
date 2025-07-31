from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from app.models import Status, Role, Priority, Method

class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class RefreshTokenRequest(BaseRequest):
    refresh_token: str


class UserUpdatePasswordRequest(BaseRequest):
    password: str


class UserCreateRequest(BaseRequest):
    phone: constr(min_length=10)
    password: constr(min_length=6)
    user_name: str | None = None
    role: Role

class ClientRegisterRequest(BaseRequest):
    client_id: int
    user_name: Optional[str] = None
    phone: str

class CarRegisterRequest(BaseRequest):
    client_id: int
    brand: str
    model: str
    number: str
    year: int

class AppRegisterRequest(BaseRequest):
    client_id: int
    car_id: int
    problem: Optional[str] = None
    conn: int

class ApplyAppAdminRequest(BaseRequest):
    admin_comment: Optional[str] = None
    status: Status
    priority: Priority
    diag_id: int

class AddUserRequest(BaseRequest):
    user_id: int
    role: Role
    user_name: str
    hashed_password: str
    phone: str

class RejectAppAdminRequest(BaseRequest):
    admin_comment: Optional[str] = None
    status: Status

class ApplyTimeAdminRequest(BaseRequest):
    arrival_time: datetime

class DiagFinishRequest(BaseRequest):
    diag_comment: Optional[str] = None
    status: Status
    diag_price: float

class MechanicFinishRequest(BaseModel):
    mechanic_comment: Optional[str] = None
    status: Status
    mechanic_price: float

class ReplacePhoneRequest(BaseModel):
    phone: str