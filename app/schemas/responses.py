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

class CheckCarResponse(BaseResponse):
    brand: str
    model: str
    number: str
    year: int

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
