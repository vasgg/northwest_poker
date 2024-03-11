from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext


from enums import States
from internal.blink1 import blink1_red
from internal.texts import replies
from keyboards import registration_keyboard
from database.models.user import User

router = Router()


@router.message(CommandStart())
async def start_message(
    message: types.Message, user: User, is_new_user: bool, state: FSMContext
) -> None:
    await state.clear()
    if is_new_user:
        await message.answer(text=replies['hello_new_user'], reply_markup=registration_keyboard)
        await blink1_red()
        return
    elif not user.nickname:
        await message.answer(text=replies['balance_without_registration'], reply_markup=registration_keyboard)
        return
    await message.answer(text=replies['hello_existing_user'])


@router.message(Command('balance'))
async def balance_command(message: types.Message, user: User, state: FSMContext) -> None:
    if not user.nickname:
        await message.answer(text=replies['balance_without_registration'], reply_markup=registration_keyboard)
        return
    await message.answer(text=replies['add_funds_reply'])
    await state.set_state(States.INPUT_AMOUNT)
