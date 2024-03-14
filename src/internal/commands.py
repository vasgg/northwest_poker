from aiogram import Bot, types

default_commands = [
    types.BotCommand(command='/start', description='начало работы'),
    types.BotCommand(command='/deposit', description='пополнить баланс'),
    types.BotCommand(command='/withdraw', description='вывод монет'),
    types.BotCommand(command='/info', description='информация'),
]


async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(default_commands)
