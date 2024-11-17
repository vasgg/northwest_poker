from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
import arrow

from database.models.user import User
from internal.enums import States
from internal.keyboards import get_info_keyboard, registration_keyboard
from internal.texts import replies

router = Router()


@router.message(CommandStart())
async def start_message(
        message: types.Message, user: User, is_new_user: bool, state: FSMContext
) -> None:
    await state.clear()
    if is_new_user:
        await message.answer(text=replies['hello_new_user'], reply_markup=registration_keyboard)
        return
    elif user.nickname:
        await message.answer(text=replies['hello_existing_user_with_nickname'])
        return
    await message.answer(text=replies['hello_existing_user'])


@router.message(Command('deposit'))
async def balance_command(message: types.Message, user: User, state: FSMContext) -> None:
    if not user.nickname:
        await message.answer(text=replies['balance_without_registration'], reply_markup=registration_keyboard)
        return
    await message.answer(text=replies['add_funds_reply'].format(settings.RATE))
    await state.set_state(States.INPUT_DEPOSIT_AMOUNT)


@router.message(Command('withdraw'))
async def withdraw_command(message: types.Message, user: User, state: FSMContext) -> None:
    if not user.nickname:
        await message.answer(text=replies['withdraw_without_registration'], reply_markup=registration_keyboard)
        return
    await message.answer(text=replies['withdraw_funds_reply'].format(settings.RATE))
    await state.set_state(States.INPUT_WITHDRAW_AMOUNT)


@router.message(Command('info'))
async def help_command(message: types.Message, user: User) -> None:
    created_at = arrow.get(user.created_at)
    await message.answer(text=replies['help_reply'].format(message.from_user.full_name,
                                                           created_at.humanize(locale='ru'),
                                                           user.id,
                                                           user.nickname if user.nickname else 'не указано',
                                                           user.telephone if user.telephone else 'не указано',
                                                           user.bank if user.bank else 'не указано'),
                         reply_markup=get_info_keyboard())

