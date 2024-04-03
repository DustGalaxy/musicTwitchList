from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Response, status, Cookie, Header
from fastapi.responses import RedirectResponse
from icecream import ic
from jose import jwt

from src.auth.schemas import TokenData, UserRead
from src.auth.utils import authenticate_user, create_access_token, get_user, twitch_login
from src.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@auth_router.get('/get_current_user')
async def get_current_user(
        session: Annotated[str | None, Cookie()] = None
) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(session, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except Exception:
        raise credentials_exception

    user = await get_user(username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


@auth_router.get("/login")
async def login_for_access_token(
        response: Response,
        authorization: Annotated[str | None, Header()] = None,
        code: Annotated[str | None, Cookie()] = None
) -> Response:
    # ic(authorization)
    if not authorization:
        authorization = code

    email_confirm_exception = HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Email not confirmed, please confirm email in Twitch to continue.",
        headers={"Authenticate": "Bearer"}
    )

    try:
        username = await twitch_login(authorization)
    except KeyError:
        raise email_confirm_exception

    user = await authenticate_user(username)

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="session", secure=True, httponly=True, value=access_token, max_age=3600)
    response.status_code = 200

    return response


@auth_router.get("/twitch/callback", response_class=RedirectResponse)
async def callback(code: str = None) -> RedirectResponse:
    response = RedirectResponse("/api/alpha1/auth/token")
    response.set_cookie("code", code, 1)
    return response
