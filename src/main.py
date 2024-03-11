import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.command_handlers import router as base_router
from handlers.errors_handler import router as errors_router
from handlers.registration_handler import router as registration_router
from handlers.balance_handler import router as balance_router
from internal.commands import set_bot_commands
from internal.notify_admin import on_shutdown_notify, on_startup_notify
from middlewares.auth_middleware import AuthMiddleware
from middlewares.session_middlewares import DBSessionMiddleware
from middlewares.updates_dumper_middleware import UpdatesDumperMiddleware
from config import get_logging_config, settings


async def main():
    logging_config = get_logging_config('northwest_poker')
    logging.config.dictConfig(logging_config)

    bot = Bot(token=settings.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    logging.info("src started")

    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage)
    dispatcher.message.middleware(DBSessionMiddleware())
    dispatcher.callback_query.middleware(DBSessionMiddleware())
    dispatcher.message.middleware(AuthMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())
    dispatcher.update.outer_middleware(UpdatesDumperMiddleware())
    dispatcher.startup.register(set_bot_commands)
    dispatcher.startup.register(on_startup_notify)
    dispatcher.shutdown.register(on_shutdown_notify)
    dispatcher.include_routers(base_router, errors_router, registration_router, balance_router)
    await dispatcher.start_polling(bot)


def run_main():
    asyncio.run(main())


if __name__ == '__main__':
    run_main()
