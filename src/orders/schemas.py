from datetime import datetime
import uuid
from pydantic import BaseModel

from src.auth.schemas import UserRead


class Order(BaseModel):
    id: uuid.UUID
    video_id: str
    title: str
    thumbnailUrl: str
    length: int
    sendler: str
    username: str
    time_created: datetime


class OrderToken(BaseModel):
    token: str
