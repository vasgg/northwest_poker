from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.records import Record
from database.models.user import User
from enums import AttachType, Status
from internal.blink1 import blink1_yellow


async def add_user_to_db(event, db_session) -> User:
    new_user = User(
        telegram_id=event.from_user.id,
        first_name=event.from_user.first_name,
        last_name=event.from_user.last_name,
        username=event.from_user.username,
    )
    db_session.add(new_user)
    await db_session.flush()
    return new_user


async def get_user_from_db(event, db_session: AsyncSession) -> User:
    query = select(User).filter(User.telegram_id == event.from_user.id)
    result: Result = await db_session.execute(query)
    user = result.scalar()
    return user


async def user_registration(user: User, nickname: str, db_session: AsyncSession) -> None:
    query = update(User).filter(User.telegram_id == user.telegram_id).values(nickname=nickname)
    await db_session.execute(query)
    await db_session.commit()


async def add_record_to_db(
        user_id: int, username: str, coins_amount: int, summ: int, rate: int, attach_id: str, attach_type: AttachType, db_session: AsyncSession
) -> Record.id:
    new_record = Record(
        user_id=user_id,
        username=username,
        rate=rate,
        coins_amount=coins_amount,
        summ=summ,
        status=Status.PENDING,
        attach_id=attach_id,
        attach_type=attach_type,
    )
    db_session.add(new_record)
    await db_session.flush()
    await blink1_yellow()
    return new_record.id
