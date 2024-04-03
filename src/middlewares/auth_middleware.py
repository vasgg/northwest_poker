import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
import gspread
import requests

from config import settings
from database.crud.user import add_user_to_db, get_user_from_db
from internal.blink1 import blink1_red
from internal.enums import Stage
from internal.google_sheet import sheet_update

logger = logging.getLogger()


class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        session = data['db_session']
        user = await get_user_from_db(event, session)
        data['is_new_user'] = False
        if not user:
            user = await add_user_to_db(event, session)
            data['is_new_user'] = True
            if settings.STAGE == Stage.PROD:
                await blink1_red()
                await sheet_update('C2', user.id)
        data['user'] = user
        return await handler(event, data)
