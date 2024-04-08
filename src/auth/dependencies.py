from datetime import datetime, timedelta, UTC
from typing import Annotated

from fastapi import Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src.auth import service
from src.auth.schemas import TokenData, UserRead
from src.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from src.auth.exceptions import CredentialsException


class AuthHandler:
    security = HTTPBearer()
    secret = SECRET_KEY

    def encode_token(self, user_name) -> str:
        payload = {
            'exp': datetime.now(tz=UTC) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)),
            'iat': datetime.now(tz=UTC),
            'sub': user_name
        }
        return jwt.encode(payload, self.secret, algorithm=ALGORITHM)

    def decode_token(self, token) -> str | None:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise CredentialsException()
        except jwt.JWTError:
            raise CredentialsException()

    async def get_current_user(
            self, auth: HTTPAuthorizationCredentials = Security(security)
    ) -> UserRead:
        username = self.decode_token(auth.credentials)
        if username is None:
            raise CredentialsException()

        user = await service.authenticate_user(username)
        if user is None:
            raise CredentialsException()
        return user
