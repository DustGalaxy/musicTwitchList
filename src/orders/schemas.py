from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict

from src.auth.schemas import UserRead


class Order(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    video_id: str
    title: str
    length: int
    sendler: str
    username: str
    time_created: datetime
    is_active: bool
    priority: int


class OrderToken(BaseModel):
    token: str


class OrderId(BaseModel):
    order_id: str
