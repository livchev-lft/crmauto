from datetime import datetime
from sqlalchemy import Enum as SQLEnum, BigInteger
from sqlalchemy import Boolean, DateTime, ForeignKey, String, func, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from enum import Enum

class Status(str, Enum):
    WAITING = "Ожидает подтверждения"
    CARWAITING = "Ожидание машины"
    DIAGNOSTIC = "На диагностике"
    REPAIR = "В ремонте"
    READY = "Готово"
    REJECTED = "Отклонена"
    COMPLETED = "Завершена"

ACTIVE_STATUSES = [
    Status.WAITING,
    Status.CARWAITING,
    Status.DIAGNOSTIC,
    Status.REPAIR,
    Status.READY
]

class Role(str, Enum):
    DIAGNOSTIC = "диагностик"
    ADMIN = "админ"
    MECHANIC = "механик"
    SUPERADMIN = "суперадмин"
    CLIENT = "клиент"

class Priority(int, Enum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1

class Method(str, Enum):
    card = "картой"
    cash = "наличка"
    unknown = "не выбран"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True)
    role: Mapped[Role] = mapped_column(SQLEnum(Role), nullable=False, default=Role.CLIENT)
    user_name: Mapped[str] = mapped_column(String(256), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    phone: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")
    diag_app = relationship("Application", back_populates="diagnostic", foreign_keys="[Application.diag_id]")
    mechanic_app = relationship("Application", back_populates="mechanic", foreign_keys="[Application.mechanic_id]")

class Client(Base):
    __tablename__ = "client_account"

    client_id: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True)
    user_name: Mapped[str] = mapped_column(String(256), nullable=True)
    phone: Mapped[str] = mapped_column(String(128), nullable=True, unique=True)

    client_app = relationship("Application", back_populates="client", foreign_keys="[Application.client_id]")
    cars = relationship("Car", back_populates="owner")

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    refresh_token: Mapped[str] = mapped_column(String(512), nullable=False, unique=True, index=True)
    used: Mapped[bool] = mapped_column(nullable=False, default=False)
    exp: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_id", ondelete="CASCADE"),)

    user: Mapped["User"] = relationship(back_populates="refresh_tokens")

class Car(Base):
    __tablename__ = "car"

    id: Mapped[int] = mapped_column(primary_key=True, nullable = False)
    client_id: Mapped[int] = mapped_column( ForeignKey("client_account.client_id"), nullable = False)
    brand: Mapped[str] = mapped_column(String(256), nullable=False)
    model: Mapped[str] = mapped_column(String(256), nullable=False)
    number: Mapped[str] = mapped_column(String(256), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    owner = relationship("Client", back_populates="cars")
    applications = relationship("Application", back_populates="car")

class Application(Base):
    __tablename__ = "application"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable = False)
    client_id: Mapped[int] = mapped_column(ForeignKey("client_account.client_id"), nullable=False)
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), nullable=False)
    problem: Mapped[str] = mapped_column(nullable=True)
    conn: Mapped[int] = mapped_column(nullable=False)
    admin_comment: Mapped[str] = mapped_column(nullable=True)
    diag_comment: Mapped[str] = mapped_column(nullable=True)
    mechanic_comment: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[Status] = mapped_column(SQLEnum(Status, name="status", create_type=False), nullable=False, default=Status.WAITING)
    priority: Mapped[Priority] = mapped_column(SQLEnum(Priority), nullable=False, default=Priority.LOW)
    diag_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_id"), nullable=True)
    mechanic_id: Mapped[int] = mapped_column(ForeignKey("user_account.user_id"), nullable=True)
    arrival_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    pay_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    diag_price: Mapped[float] = mapped_column(Float, nullable=True)
    mechanic_price: Mapped[float] = mapped_column(Float, nullable=True)

    car = relationship("Car", back_populates="applications")
    client = relationship("Client", back_populates="client_app", foreign_keys=[client_id])
    diagnostic = relationship("User", back_populates="diag_app", foreign_keys=[diag_id])
    mechanic = relationship("User", back_populates="mechanic_app", foreign_keys=[mechanic_id])
    payment = relationship("Payment", back_populates="application", uselist=False)

class Payment(Base):
    __tablename__ = "payment"

    application_id: Mapped[int] = mapped_column(ForeignKey("application.id"), primary_key=True, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    payment_method: Mapped[Method] = mapped_column(SQLEnum(Method), nullable=True, default=Method.unknown)
    pay_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    application = relationship("Application", back_populates="payment")
