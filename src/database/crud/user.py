from sqlalchemy import Result, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.records import Record
from database.models.user import User
from internal.enums import AttachType, OperationType, Status


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


async def get_user_by_id(user_id: int, db_session: AsyncSession) -> User:
    query = select(User).filter(User.id == user_id)
    result: Result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    return user


async def user_registration(user: User, nickname: str, db_session: AsyncSession) -> None:
    query = update(User).filter(User.telegram_id == user.telegram_id).values(nickname=nickname)
    await db_session.execute(query)
    await db_session.commit()


async def add_record_to_db(
        user_id: int,
        username: str,
        operation: OperationType,
        status: Status,
        coins_amount: int,
        summ: int,
        rate: int,
        db_session: AsyncSession,
        attach_id: str | None = None,
        attach_type: AttachType | None = None,
) -> Record.id:
    new_record = Record(
        user_id=user_id,
        username=username,
        operation=operation,
        rate=rate,
        coins_amount=coins_amount,
        summ=summ,
        status=status,
        attach_id=attach_id,
        attach_type=attach_type,
    )
    db_session.add(new_record)
    await db_session.flush()
    return new_record.id
