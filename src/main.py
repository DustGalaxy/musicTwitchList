from typing import Annotated, Dict
from urllib.parse import urlencode

from fastapi import APIRouter, FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.auth.router import auth_router, get_current_user
from src.auth.schemas import UserRead
from src.auth.models import User

from src.orders.router import order_router

from src.config import TWITCH_CLIENT_ID, REDIRECT_URL, TWITCH_URL_AUTHORIZE


request_payload = { 
            "client_id": TWITCH_CLIENT_ID,
            "force_verify": 'false',
            "redirect_uri": "http://localhost:8000/api/alpha1/auth/twitch/callback",
            "response_type": 'code',
            "scope": 'user:read:email'
            }

url = TWITCH_URL_AUTHORIZE + '?' + urlencode(request_payload)

app = FastAPI()

api_router = APIRouter(
    prefix='/api',
    tags=['Api'],
)

alpha1 = APIRouter(
    prefix='/alpha1',
    tags=['Alpha1'],
)


@alpha1.get("/users/me/", response_model=UserRead)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user



@alpha1.get("/users/me/config")
async def get_user_config(current_user: Annotated[User, Depends(get_current_user)]) -> Dict[str, str]:
    return current_user.config


alpha1.include_router(auth_router)
alpha1.include_router(order_router)

api_router.include_router(alpha1)

app.include_router(api_router)

origins = ['http://localhost:3000', 'http://127.0.0.1:3000',
           'https://localhost:3000', 'https://127.0.0.1:3000'] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index() -> HTMLResponse:
    return HTMLResponse(f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                        </head>
                        <body>
                        <a href="{url}">log</a>
                        </body>
                        </html>
                        """)




