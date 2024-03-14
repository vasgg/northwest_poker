from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.records import Record


async def get_record_by_id(record_id: int, db_session: AsyncSession) -> Record:
    query = select(Record).filter(Record.id == record_id)
    result: Result = await db_session.execute(query)
    record = result.scalar()
    return record
