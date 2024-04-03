from datetime import datetime, timedelta, timezone
from typing import Literal

from icecream import ic
from jose import jwt
from sqlalchemy import insert, select, update
from src.config import SECRET_KEY, TWITCH_CLIENT_ID, ALGORITHM, REDIRECT_URL
from src.auth.models import User, Credentials
from src.auth.manager import client
from src.database import async_session_maker
from fastapi import HTTPException


async def get_user(username: str) -> User | None:
    async with async_session_maker() as session:
        stmt = select(User).filter(User.username.ilike(username))
        user = await session.execute(statement=stmt)
        user = user.scalar_one_or_none()
        return user


async def authenticate_user(username: str) -> User | Literal[False]:
    user = await get_user(username)
    if not user:
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def twitch_login(code: str = None) -> str:
    try:
        token = await client.get_access_token(code, REDIRECT_URL)
    except Exception:
        raise HTTPException(400, "missing code")

    data = await client.get_id_email(token["access_token"])

    user_data = await client.get_user_data(token["access_token"], TWITCH_CLIENT_ID, data[0])
    user_data = user_data["data"][0]

    async with async_session_maker() as session:
        stmt = select(User).join(Credentials).where(Credentials.twitch_user_id == data[0])
        user = await session.execute(stmt)

        user = user.scalar_one_or_none()

        if user is None:
            stmt = insert(User).values(
                username=user_data["display_name"],
                registered_at=datetime.now(timezone.utc),
                image_url=user_data["profile_image_url"],
                email=user_data["email"],

            ).returning(User)

            user = await session.execute(stmt)
            user = user.scalar_one()
            stmt2 = insert(Credentials).values(
                username=user.username,
                twitch_user_id=data[0],
                twitch_access_token=token["access_token"],
                twitch_refresh_token=token["refresh_token"],
            )
            await session.execute(stmt2)
            await session.commit()

        elif user.image_url != user_data["profile_image_url"]:

            stmt = update(User).where(User.id == user.id).values(
                image_url=user_data["profile_image_url"]
            )
            await session.execute(stmt)
            await session.commit()

    return user.username
