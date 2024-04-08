from datetime import timedelta
from typing import Annotated, Dict

from fastapi import APIRouter, HTTPException, Response, status, Cookie, Header
from fastapi.responses import RedirectResponse
from icecream import ic
from jose import jwt

from src.auth import service
from src.auth.schemas import TokenData, UserRead
from src.auth.dependencies import AuthHandler
from src.auth.exceptions import MissingCode, EmailConfirmException
from src.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

auth_handler = AuthHandler()


@auth_router.get("/login")
async def login_for_access_token(
        response: Response,
        authorization: Annotated[str | None, Header()] = None,
        code: Annotated[str | None, Cookie()] = None
) -> dict[str, str]:
    if not authorization:
        if code is None:
            raise MissingCode()
        authorization = code

    ic(authorization)

    try:
        username = await service.twitch_login(authorization)
    except KeyError:
        raise EmailConfirmException()

    user = await service.authenticate_user(username)

    access_token = auth_handler.encode_token(user.username)

    # response.set_cookie(key="session", secure=True, httponly=True, value=access_token, max_age=3600)
    # response.status_code = 200
    return {'token': access_token}


@auth_router.get("/twitch/callback", response_class=RedirectResponse)
async def callback(code: str = None) -> RedirectResponse:
    response = RedirectResponse("/api/v1/auth/login")
    response.set_cookie("code", code, 1)
    return response
