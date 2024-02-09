from datetime import datetime, timedelta
from typing import Annotated
from fastapi.responses import RedirectResponse
from jose import jwt
from src.auth.utils import authenticate_user, create_access_token, get_user, twitch_login
from src.auth.schemas import Token, TokenData, UserRead
from src.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from fastapi import APIRouter, HTTPException, Response, status, Cookie

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@auth_router.get('/get_current_user')
async def get_current_user(session: Annotated[str | None, Cookie()] = None) -> UserRead:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
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


@auth_router.get("/token", response_model=Token)
async def login_for_access_token(code: Annotated[str | None, Cookie()] = None) -> Token:
    response = RedirectResponse("/api/users/me/")
    try:
        username = await twitch_login(code)
    except KeyError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        raise HTTPException(503, {"detail": "Email not confirmed, please confirm email to continue."}) 
    user = await authenticate_user(username)

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="session", secure=True, httponly=True, value=access_token, max_age=3600)
    
    # todo normal return
    return response



@auth_router.get("/twitch/callback", response_class=RedirectResponse)
async def callback(code: str = None)-> RedirectResponse:
    
    response = RedirectResponse("/api/alpha1/auth/token")
    response.set_cookie("code", code, 1)
        
    return response



