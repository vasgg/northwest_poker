from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import Base
from src.enums import Status


class Record(Base):
    __tablename__ = 'records'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    username: Mapped[str]
    rate: Mapped[int]
    coins_amount: Mapped[int]
    summ: Mapped[int]
    status: Mapped[Status]
    image_id: Mapped[str]
