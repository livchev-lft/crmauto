from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from app.models import Status, Role, Priority, Method

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class AccessTokenResponse(BaseResponse):
    token_type: str = "Bearer"
    access_token: str
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int

class UserResponse(BaseResponse):
    user_id: str
    email: EmailStr

class NewAppToAdminResponse(BaseResponse):
    id: int
    number: str
    client_id: int
    brand: str
    model: str
    year: int
    problem: Optional[str] = None

class CheckClient(BaseResponse):
    client_id: int
    user_name: Optional[str]
    phone: str

    model_config = ConfigDict(from_attributes=True)

class CheckCarResponse(BaseResponse):
    id: int
    brand: str
    model: str
    number: str
    year: int

    model_config = ConfigDict(from_attributes=True)

class DiagGetAppResponse(BaseResponse):
    cleint_id: int
    car_id: int
    arrival_time: datetime
    priority: str
    problem: Optional[str] = None
    admin_comment: Optional[str] = None

class MechanicGetResponse(BaseResponse):
    cleint_id: int
    car_id: int
    problem: str
    admin_comment: str
    diag_commnt: str
    priority: Priority

class AdminGetFinishAppResponse(BaseResponse):
    app_id: int

class GetAppsResponse(BaseResponse):
    id: int
    car_id: int
    problem: str
    conn: int
    admin_comment: Optional[str] = None
    diag_comment: Optional[str] = None
    mechanic_comment: Optional[str] = None
    status: Status = Status.WAITING
    arrival_time: Optional[datetime] = None
    created_at: datetime
    diag_price: Optional[float] = None
    mechanic_price: Optional[float] = None

class AdminGetStartAppResponse(BaseResponse):
    app_id: int
    client_id: int
    car_id: int
    problem: str
    conn: int
    phone: str
    brand: str
    model: str
    number: str
    year: int

class AppListItem(BaseResponse):
    id: int
    client_id: int
    car_id: int
    problem: str
    conn: int
    created_at: datetime
    car: CheckCarResponse
    client: CheckClient

    model_config = ConfigDict(from_attributes=True)

class DiagNamesList(BaseResponse):
    user_id: int
    user_name: str