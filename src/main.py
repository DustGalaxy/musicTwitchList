from typing import Annotated, Dict
from urllib.parse import urlencode

import uvicorn
from jose import jwt, JWTError

from fastapi import APIRouter, Depends, FastAPI, Response, Cookie, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import update
from starlette import status

from src.auth.router import auth_router, get_current_user
from src.auth.schemas import UserRead
from src.auth.models import User

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import get_user
from src.database import get_async_session

from src.config import TWITCH_CLIENT_ID, REDIRECT_URL, TWITCH_URL_AUTHORIZE, SECRET_KEY, ALGORITHM
from src.orders.router import order_router
from src.my_awesome_sockets import sio_app, sio_server
from src.statistic.router import statistic_router

request_payload = {
    "client_id": TWITCH_CLIENT_ID,
    "force_verify": 'false',
    "redirect_uri": REDIRECT_URL,
    "response_type": 'code',
    "scope": 'user:read:email'
}

url = TWITCH_URL_AUTHORIZE + '?' + urlencode(request_payload)

app = FastAPI()
app.mount('/ws', app=sio_app)

origins = ['http://localhost:5173', 'http://127.0.0.1:5173',
           'https://localhost:5173', 'https://127.0.0.1:5173']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(
    prefix='/api',
    tags=['Api'],
)

alpha1 = APIRouter(
    prefix='/alpha1',
    tags=['Alpha1'],
)


@alpha1.get("/users/me", response_model=UserRead)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@alpha1.get("/users/get_config")
async def get_user_config(
        session: Annotated[str | None, Cookie()] = None
) -> dict[str, int | str]:

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
    except JWTError:
        raise credentials_exception

    user = await get_user(username)
    return user.config


@alpha1.post("/users/set_config")
async def get_user_config(
        config: Dict[str, str],
        current_user: Annotated[User, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_async_session)]
) -> Dict[str, str]:
    stmt = update(User).where(User.id == current_user.id).values(config=config)
    await session.execute(stmt)
    await session.commit()

    return {"detail": "Config was updated"}


@alpha1.get("/login")
async def home():
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
    </head>
    <body>
    <a href={url}> Login </a>
    </body>
    </html>
    """)

alpha1.include_router(statistic_router)
alpha1.include_router(auth_router)
alpha1.include_router(order_router)
api_router.include_router(alpha1)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)
