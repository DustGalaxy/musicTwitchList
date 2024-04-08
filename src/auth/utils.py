from fastapi import HTTPException

from src.config import TWITCH_CLIENT_ID, REDIRECT_URL
from src.auth.manager import client
from src.auth.exceptions import MissingCode


async def get_token_for_twitch(
        code: str
) -> dict[str, str]:
    try:
        token = await client.get_access_token(code, REDIRECT_URL)
    except Exception:
        raise MissingCode
    else:
        return token


async def get_user_data_from_twitch(
        token: dict[str, str]
) -> dict[str, str | int]:
    twitch_id = await client.get_id(token["access_token"])
    user_data = await client.get_user_data(token["access_token"], TWITCH_CLIENT_ID, twitch_id)
    return user_data
