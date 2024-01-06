from typing import Annotated, Dict
from urllib.parse import urlencode

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse

from src.auth.router import auth_router, get_current_user
from src.auth.schemas import UserRead
from src.auth.models import User

from src.orders.router import order_router

from src.config import TWITCH_CLIENT_ID, REDIRECT_URL, TWITCH_URL_AUTHORIZE


request_payload = { 
            "client_id": TWITCH_CLIENT_ID,
            "force_verify": 'false',
            "redirect_uri": REDIRECT_URL,
            "response_type": 'code',
            "scope": 'user:read:email'
            }

url = TWITCH_URL_AUTHORIZE + '?' + urlencode(request_payload)

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


@app.get("/users/me/", response_model=UserRead)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_user)]) -> list[dict[str, str]]:
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/users/me/config")
async def get_user_config(current_user: Annotated[User, Depends(get_current_user)]) -> Dict[str, str]:
    return current_user.config

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




