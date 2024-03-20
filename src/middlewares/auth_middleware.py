import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
import gspread
import requests

from database.crud.user import add_user_to_db, get_user_from_db
from internal.google_sheet import update_google_sheet

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
            try:
                await update_google_sheet('B2', user.id)
                logger.info(f'google sheet is updated with value {user.id}')
            except gspread.exceptions.APIError as e:
                logger.error(f'API Google Sheets error: {e}', exc_info=True)
            except requests.exceptions.RequestException as e:
                logger.error(f'Network error while updating Google Sheets: {e}', exc_info=True)
            except Exception as e:
                logger.exception(f'Unexpected error while updating Google Sheet: {e}')
            data['is_new_user'] = True
        data['user'] = user
        return await handler(event, data)
