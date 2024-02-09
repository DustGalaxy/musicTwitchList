from typing import Any, Dict, List, Optional, Tuple, override
from httpx_oauth.clients.openid import BASE_SCOPES, OpenID
from src.config import TWITCH_CLIENT_ID, TWITCH_SECRET
from httpx_oauth.errors import GetIdEmailError

class MyOpenID(OpenID):
    def __init__(self, client_id: str, client_secret: str, openid_configuration_endpoint: str, name: str = "openid", base_scopes: List[str] | None = BASE_SCOPES) -> None:
        super().__init__(client_id, client_secret, openid_configuration_endpoint, name, base_scopes)
        
    @override
    async def get_id_email(self, token: str) -> Tuple[str, Optional[str]]:
        async with self.get_httpx_client() as client:
            response = await client.get(
                self.openid_configuration["userinfo_endpoint"],
                headers={**self.request_headers, 
                            "Authorization": f"Bearer {token}", 
                            }, 
            )
            
            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            data: Dict[str, Any] = response.json()
            user_info = await self.get_user_data(token, self.client_id, data["sub"])
            
            return str(data["sub"]), user_info["data"][0]["email"]
        
    async def get_user_data(self, token: str, client_id: str, user_id: int) -> Dict[str, Any]:
        async with self.get_httpx_client() as client:
            response = await client.get(
                "https://api.twitch.tv/helix/users",
                headers={**self.request_headers, 
                            "Authorization": f"Bearer {token}", 
                            "Client-id": f"{client_id}"
                            },  
                params={"id": user_id}  
            )
            
            if response.status_code >= 400:
                raise GetIdEmailError(response.json())

            data: Dict[str, Any] = response.json()
            return data

client = MyOpenID(TWITCH_CLIENT_ID, TWITCH_SECRET, "https://id.twitch.tv/oauth2/.well-known/openid-configuration")
