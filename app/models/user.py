import datetime
from enum import Enum
from sqlalchemy import String, Numeric, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class UserRole(str, Enum):
    CLIENT = "client"
    FREELANCER = "freelancer"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CLIENT, nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    # Bog'liqliklar
    gigs: Mapped[list["Gig"]] = relationship("Gig", back_populates="freelancer", cascade="all, delete-orphan")
    orders_as_client: Mapped[list["Order"]] = relationship("Order", foreign_keys="Order.client_id",
                                                           back_populates="client")
    orders_as_freelancer: Mapped[list["Order"]] = relationship("Order", foreign_keys="Order.freelancer_id",
                                                               back_populates="freelancer")
