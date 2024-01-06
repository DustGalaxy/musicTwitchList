import uuid
from pydantic import BaseModel

from src.auth.schemas import UserRead

class Order(BaseModel):
    id: uuid.UUID
    url: str
    sendler: str
    recipient: UserRead