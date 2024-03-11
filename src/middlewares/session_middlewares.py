from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.exc import PendingRollbackError

from database.db import db


class DBSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with db.session_factory() as db_session:
            data['db_session'] = db_session
            res = await handler(event, data)
            try:
                await db_session.commit()
            except PendingRollbackError:
                ...
            return res
