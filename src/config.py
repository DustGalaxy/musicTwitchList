from dotenv import load_dotenv
import os

load_dotenv()


TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_SECRET = os.environ.get("TWITCH_SECRET")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
SECRET_KEY = os.environ.get("SECRET_KEY")

ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")

REDIRECT_URL = os.environ.get("REDIRECT_URL")
TWITCH_URL_AUTHORIZE = os.environ.get("TWITCH_URL_AUTHORIZE")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")