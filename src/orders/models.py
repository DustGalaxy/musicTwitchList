from datetime import datetime, timezone
from uuid import uuid4
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import DateTime, ForeignKey, Boolean, Integer
from src.database import Base
from sqlalchemy.orm import Mapped, relationship, MappedColumn


class Order(Base):
    __tablename__ = "order"

    id: Mapped[UUID_ID] = MappedColumn(GUID, primary_key=True, default=uuid4)

    video_id: Mapped[str]
    title: Mapped[str]
    length: Mapped[int]
    sendler: Mapped[str]

    time_created = MappedColumn(DateTime(timezone=True), default=datetime.now(timezone.utc))

    username: Mapped[str] = MappedColumn(ForeignKey('user.username'))
    user: Mapped["User"] = relationship(back_populates="order")

    is_active: Mapped[bool] = MappedColumn(Boolean, default=True)
    priority: Mapped[int] = MappedColumn(Integer, default=1, nullable=True)
