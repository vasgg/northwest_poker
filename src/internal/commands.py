from aiogram import Bot, types

default_commands = [
    types.BotCommand(command='/start', description='начало работы'),
    types.BotCommand(command='/balance', description='пополнить баланс'),
]

# special_commands = [
#     types.BotCommand(command='/start', description='start src'),
#     types.BotCommand(command='/position', description='set slide position'),
#     types.BotCommand(command='/paywall', description='toggle paywall access'),
#     types.BotCommand(command='/reminders', description='set src reminders'),
# ]


async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(default_commands)
