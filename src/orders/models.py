

from uuid import UUID
from src.auth.models import User
from src.database import Base
from sqlalchemy.orm import Mapped, relationship, MappedColumn

class Order(Base):
    __tablename__ = "order"
    id: UUID
    url: str
    sendler: str
    recipient: Mapped[User] = relationship("User", lazy="joined")