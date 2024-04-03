from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, MappedColumn, relationship

from src.database import Base


class StatisticConfig(Base):
    __tablename__ = "statistic_config"

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True)

    username: Mapped[str] = MappedColumn(ForeignKey('user.username'))
    user: Mapped["User"] = relationship(back_populates="statistic_config")

    to_global_statistic: Mapped[bool] = MappedColumn(Boolean, default=True)









