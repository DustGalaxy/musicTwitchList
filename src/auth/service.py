from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import HTTPException
from icecream import ic
from jose import jwt

from src.config import SECRET_KEY, TWITCH_CLIENT_ID, ALGORITHM, REDIRECT_URL
from src.auth.models import User, Credentials
from src.auth.schemas import UserRegister
from src.auth.manager import client
from src.auth.repo import fetch_user_by_twitch_user_id, update_profile_image_url, fetch_user, register_user
from src.auth.utils import get_user_data_from_twitch, get_token_for_twitch


async def authenticate_user(username: str) -> User | None:
    user = await fetch_user(username)
    if not user:
        return None
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

    token = await get_token_for_twitch(code)
    user_data = await get_user_data_from_twitch(token)
    user = await fetch_user_by_twitch_user_id(user_data["id"])

    if user is None:
        user = register_user(UserRegister(
            username=user_data["display_name"],
            image_url=user_data["profile_image_url"],
            email=user_data["email"],
            twitch_user_id=user_data["id"],
            twitch_access_token=token["access_token"],
            twitch_refresh_token=token["refresh_token"],
        ))

    elif user.image_url != user_data["profile_image_url"]:
        await update_profile_image_url(user.id, user_data["profile_image_url"])

    return user.username
