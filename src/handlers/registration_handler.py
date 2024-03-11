import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud.user import user_registration
from database.models.user import User
from enums import Entities, States
from internal.texts import replies
from keyboards import get_confirmation_keyboard, registration_keyboard

router = Router()
logger = logging.getLogger()


@router.callback_query(F.data == 'registration')
async def start_registration(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.answer(text=replies['registration_nick'])
    await state.set_state(States.INPUT_NICK)


@router.message(States.INPUT_NICK)
async def input_nick(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=replies['registration_nick_confirmation'].format(message.text),
                         reply_markup=get_confirmation_keyboard(mode=Entities.NICK))
    await state.update_data(nick=message.text)
    await state.set_state()


@router.callback_query(F.data == 'confirm_nick')
async def confirm_nick(call: types.CallbackQuery, user: User, db_session: AsyncSession, state: FSMContext) -> None:
    await call.answer()
    await call.message.answer(text=replies['registration_сomplete'])
    data = await state.get_data()
    await user_registration(user=user, nickname=data['nick'], db_session=db_session)
    logger.info(f'User {user.id} registered. Nickname: {data["nick"]}')
    await state.set_state()


@router.callback_query(F.data == 'change_nick')
async def change_nick(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.answer(text=replies['registration_nick'])
    await state.set_state(States.INPUT_NICK)
