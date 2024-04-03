import os

from aiogram import Bot
from config import settings


async def on_startup_notify(bot: Bot):
    await bot.send_message(
        settings.ADMINS[0],
        f'{os.getcwd().split(os.sep)[-1].capitalize()} started\n\n/start',
        disable_notification=True,
    )


async def on_shutdown_notify(bot: Bot):
    await bot.send_message(
        settings.ADMINS[0], f'{os.getcwd().split(os.sep)[-1].capitalize()} shutdown', disable_notification=True,
    )
