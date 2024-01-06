
from datetime import datetime, timedelta
from typing import Literal, Optional
from jose import jwt
from sqlalchemy import insert, select
from src.config import SECRET_KEY, TWITCH_CLIENT_ID, ALGORITHM
from src.auth.models import User
from src.auth.manager import client
from src.database import async_session_maker
from fastapi import HTTPException

redirect_uri = "http://localhost:8000/auth/twitch/callback"




async def get_user(username: str) -> User | None:
    async with async_session_maker() as session:
        stmt = select(User).where(User.username == username)
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
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def twitch_login(code: str = None) -> str:
    
    try:
        token = await client.get_access_token(code, redirect_uri)
    except Exception:
        raise HTTPException(400, "missing code")

    data = await client.get_id_email(token["access_token"])

    user_data = await client.get_user_data(token["access_token"], TWITCH_CLIENT_ID, data[0])
    user_data = user_data["data"][0]


    async with async_session_maker() as session:
        stmt = select(User).where(User.twitch_user_id == data[0])
        user = await session.execute(stmt)
        await session.commit()
    
        user = user.scalar_one_or_none()

        if (user is None):

            stmt = insert(User).values(
                username = user_data["display_name"],
                registered_at = datetime.utcnow(),
                twitch_user_id = data[0],
                twitch_access_token = token["access_token"],
                twitch_refresh_token = token["refresh_token"],
                image_url = user_data["profile_image_url"],
                email = user_data["email"]
            )
        
            await session.execute(stmt)
            await session.commit()
        
            stmt = select(User).where(User.username == user_data["display_name"])
            user = await session.execute(stmt)
            user = user.scalar_one()
        
    return user.username