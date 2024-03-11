from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.enums import Entities

registration_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='регистрация', callback_data='registration'),
        ],
    ],
)


def get_confirmation_keyboard(mode: Entities) -> InlineKeyboardMarkup:
    match mode:
        case Entities.NICK:
            confirm_data = 'confirm_nick'
            change_data = 'change_nick'
        case Entities.AMOUNT:
            confirm_data = 'confirm_amount'
            change_data = 'change_amount'
        case _:
            assert False, 'Unexpected mode'
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='☑️ подтвердить', callback_data=confirm_data),
                InlineKeyboardButton(text='🔄 изменить', callback_data=change_data),
            ],
        ],
    )
