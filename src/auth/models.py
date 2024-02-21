from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID

from sqlalchemy import TIMESTAMP, Boolean, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from src.config import DEFAULT_BOT_CONFIG
from src.orders.models import Order

from src.database import Base


class User(Base):
    __tablename__ = "user"
    
    id: Mapped[UUID_ID] = MappedColumn(GUID, primary_key=True, default=uuid4)
    username:  Mapped[str] = MappedColumn(String, unique=True, nullable=False)
    email: Mapped[str] = MappedColumn(String, nullable=False)
    registered_at = MappedColumn(TIMESTAMP, default=datetime.utcnow)

    image_url: Mapped[str] = MappedColumn(String, nullable=False)
    config: Mapped[dict] = MappedColumn(JSON, nullable=True, default=DEFAULT_BOT_CONFIG)
    
    twitch_user_id: Mapped[str] = MappedColumn(String, nullable=False)
    twitch_access_token: Mapped[str] = MappedColumn(String, nullable=False)
    twitch_refresh_token: Mapped[str] = MappedColumn(String, nullable=False)
    is_active: Mapped[bool] = MappedColumn(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = MappedColumn(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = MappedColumn(Boolean, default=False, nullable=False)
    
    order: Mapped[List["Order"]] = relationship()

