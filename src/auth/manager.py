from httpx_oauth.clients.openid import OpenID
from src.config import TWITCH_CLIENT_ID, TWITCH_SECRET, SECRET_AUTH


client = OpenID(TWITCH_CLIENT_ID, TWITCH_SECRET, "https://id.twitch.tv/oauth2/.well-known/openid-configuration")
