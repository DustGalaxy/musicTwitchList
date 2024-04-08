from typing import Annotated

from fastapi import Depends
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

from src.auth.models import User, Credentials
from src.auth.schemas import UserRegister
from src.database import async_session_maker


async def fetch_user(
        username: str,
        db_session: AsyncSession = async_session_maker()
) -> User | None:
    stmt = select(User).filter(User.username.ilike(username))
    user = await db_session.execute(statement=stmt)
    user = user.scalar_one_or_none()
    return user


async def fetch_user_by_twitch_user_id(
        twitch_user_id: str,
        db_session: AsyncSession = async_session_maker()
) -> User | None:
    stmt = select(User).join(Credentials).where(Credentials.twitch_user_id == twitch_user_id)
    user = await db_session.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def register_user(
        user_data: UserRegister,
        db_session: AsyncSession = async_session_maker()
) -> User:
    stmt = insert(User).values(
        username=user_data.username,
        image_url=user_data.image_url,
        email=user_data.email,
    ).returning(User)

    stmt2 = insert(Credentials).values(
        username=user_data.username,
        twitch_user_id=user_data.twitch_user_id,
        twitch_access_token=user_data.twitch_access_token,
        twitch_refresh_token=user_data.twitch_refresh_token,
    )
    await session.execute(stmt2)

    return await db_session.execute(stmt).scalar_one()


async def update_profile_image_url(
        user_id: uuid.UUID,
        profile_image_url: str,
        db_session: AsyncSession = async_session_maker()
) -> None:
    stmt = update(User).where(User.id == user_id).values(
        image_url=profile_image_url
    )
    await db_session.execute(stmt)
    await db_session.commit()
