from datetime import datetime
from typing import Any, Generator
from uuid import uuid4
import uuid

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import UUID_ID, SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.generics import GUID

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import TIMESTAMP, Boolean, Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, MappedColumn

from src.database import Base, get_async_session


class User(Base):
    __tablename__ = "user"
    
    id: Mapped[UUID_ID] = MappedColumn(GUID, primary_key=True, default=uuid.uuid4)
    username:  Mapped[str] = MappedColumn(String, nullable=False)
    email: Mapped[str] = MappedColumn(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)

    image_url: Mapped[str] = MappedColumn(String, nullable=False)
    
    twitch_user_id: Mapped[str] = MappedColumn(String, nullable=False)
    twitch_access_token: Mapped[str] = MappedColumn(String, nullable=False)
    twitch_refresh_token: Mapped[str] = MappedColumn(String, nullable=False)
    is_active: Mapped[bool] = MappedColumn(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = MappedColumn(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = MappedColumn(Boolean, default=False, nullable=False)


async def get_user_db(session: AsyncSession = Depends(get_async_session))-> Generator[SQLAlchemyUserDatabase[User, Any], Any, None]:
    yield SQLAlchemyUserDatabase(session, User)