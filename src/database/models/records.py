from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base
from internal.enums import OperationType, Status, AttachType


class Record(Base):
    __tablename__ = 'records'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    username: Mapped[str]
    rate: Mapped[int]
    coins_amount: Mapped[int]
    summ: Mapped[int]
    status: Mapped[Status]
    operation: Mapped[OperationType]
    attach_type: Mapped[AttachType | None]
    attach_id: Mapped[str | None]
    message_id: Mapped[int | None]
