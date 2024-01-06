from datetime import datetime
from uuid import uuid4
from fastapi_users_db_sqlalchemy import UUID_ID
from fastapi_users_db_sqlalchemy.generics import GUID
from sqlalchemy import TIMESTAMP, ForeignKey
from src.database import Base
from sqlalchemy.orm import Mapped, relationship, MappedColumn

class Order(Base):
    __tablename__ = "order"
    id: Mapped[UUID_ID] = MappedColumn(GUID, primary_key=True, default=uuid4)
    url: Mapped[str] 
    sendler: Mapped[str] 
    time_created = MappedColumn(TIMESTAMP, default=datetime.utcnow)
    user_id: Mapped[UUID_ID] = MappedColumn(ForeignKey('user.id'))
    