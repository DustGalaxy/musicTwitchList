from datetime import datetime
from uuid import uuid4
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import TIMESTAMP, ForeignKey
from src.database import Base
from sqlalchemy.orm import Mapped, relationship, MappedColumn


class Order(Base):
    __tablename__ = "order"
    id: Mapped[UUID_ID] = MappedColumn(GUID, primary_key=True, default=uuid4)
    video_id: Mapped[str]
    title: Mapped[str]
    thumbnailUrl: Mapped[str]
    length: Mapped[int]
    sendler: Mapped[str]
    time_created = MappedColumn(TIMESTAMP, default=datetime.utcnow)
    username: Mapped[str] = MappedColumn(ForeignKey('user.username'), nullable=True)
    user: Mapped["User"] = relationship(back_populates="order")
