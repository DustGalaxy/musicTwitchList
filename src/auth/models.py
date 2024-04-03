from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID

from sqlalchemy import TIMESTAMP, Boolean, String, UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from src.config import DEFAULT_BOT_CONFIG
from src.orders.models import Order

from src.database import Base
from src.statistic.models import StatisticConfig


class User(Base):
    __tablename__ = "user"

    id: Mapped[UUID_ID] = MappedColumn(GUID, primary_key=True, default=uuid4)
    username:  Mapped[str] = MappedColumn(String, unique=True, nullable=False)
    email: Mapped[str] = MappedColumn(String, nullable=False)
    registered_at = MappedColumn(TIMESTAMP, default=datetime.now(timezone.utc))

    image_url: Mapped[str] = MappedColumn(String, nullable=False)
    config: Mapped[dict] = MappedColumn(JSON, nullable=True, default=DEFAULT_BOT_CONFIG)

    is_active: Mapped[bool] = MappedColumn(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = MappedColumn(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = MappedColumn(Boolean, default=False, nullable=False)
    in_statistics: Mapped[bool] = MappedColumn(Boolean, default=True, nullable=True)

    order: Mapped[List["Order"]] = relationship()
    credentials: Mapped[List["Credentials"]] = relationship()
    statistic_config: Mapped["StatisticConfig"] = relationship(back_populates='user')


class Credentials(Base):
    __tablename__ = "credentials"

    id: Mapped[UUID_ID] = MappedColumn(GUID, primary_key=True, default=uuid4)

    username: Mapped[str] = MappedColumn(ForeignKey('user.username'))
    user: Mapped["User"] = relationship(back_populates="credentials")

    twitch_user_id: Mapped[str] = MappedColumn(String, nullable=False)
    twitch_access_token: Mapped[str] = MappedColumn(String, nullable=False)
    twitch_refresh_token: Mapped[str] = MappedColumn(String, nullable=False)
