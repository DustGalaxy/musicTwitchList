from typing import Any, Dict, List, Optional, Tuple, override

from httpx_oauth.clients.openid import BASE_SCOPES, OpenID
from httpx_oauth.errors import GetIdEmailError
from icecream import ic

from src.config import TWITCH_CLIENT_ID, TWITCH_SECRET


class MyOpenID(OpenID):
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            openid_configuration_endpoint: str,
            name: str = "openid",
            base_scopes: List[str] | None = BASE_SCOPES
    ) -> None:
        super().__init__(
            client_id,
            client_secret,
            openid_configuration_endpoint,
            name,
            base_scopes)

    async def get_id(self, token: str) -> str:
        async with self.get_httpx_client() as tmp_client:
            response = await tmp_client.get(
                url=self.openid_configuration["userinfo_endpoint"],
                headers={
                    **self.request_headers,
                    "Authorization": f"Bearer {token}"
                },
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            data: Dict[str, Any] = response.json()

            return str(data["sub"])

    async def get_user_data(self, token: str, client_id: str, user_id: int) -> Dict[str, Any]:
        async with self.get_httpx_client() as tmp_client:
            response = await tmp_client.get(
                "https://api.twitch.tv/helix/users",
                headers={
                    **self.request_headers,
                    "Authorization": f"Bearer {token}",
                    "Client-id": f"{client_id}"
                },
                params={"id": user_id}
            )

            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            data: Dict[str, Any] = response.json()
            return data["data"][0]


client = MyOpenID(TWITCH_CLIENT_ID, TWITCH_SECRET, "https://id.twitch.tv/oauth2/.well-known/openid-configuration")
