import datetime
from enum import Enum
from sqlalchemy import Numeric, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class OrderStatus(str, Enum):
    PENDING_PAYMENT = "pending_payment"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gig_id: Mapped[int] = mapped_column(ForeignKey("gigs.id"), nullable=False)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    freelancer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.PENDING_PAYMENT,
                                                nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow,
                                                          onupdate=datetime.datetime.utcnow)

    gig: Mapped["Gig"] = relationship("Gig", back_populates="orders")
    client: Mapped["User"] = relationship("User", foreign_keys=[client_id], back_populates="orders_as_client")
    freelancer: Mapped["User"] = relationship("User", foreign_keys=[freelancer_id],
                                              back_populates="orders_as_freelancer")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="order", cascade="all, delete-orphan")