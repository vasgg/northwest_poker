import logging

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database.crud.record import get_record_by_id
from database.crud.user import add_record_to_db, user_registration
from database.models.user import User
from internal.enums import Entities, OperationType, States, Status
from internal.texts import replies
from internal.keyboards import get_confirmation_keyboard, get_operation_keyboard

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
    await call.message.edit_reply_markup()
    data = await state.get_data()
    await user_registration(user=user, nickname=data['nick'], db_session=db_session)
    logger.info(f'User {user.id} registered. Nickname: {data["nick"]}')
    await call.message.answer(text=replies['registration_сomplete'])
    await state.set_state()


@router.callback_query(F.data == 'change_nick')
async def change_nick(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(text=replies['registration_nick'])
    await state.set_state(States.INPUT_NICK)


@router.message(States.INPUT_WITHDRAW_TELEPHONE)
async def input_withdraw_telephone(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=replies['withdraw_telephone_confirmation'].format(message.text),
                         reply_markup=get_confirmation_keyboard(mode=Entities.WITHDRAW_TELEPHONE))
    await state.update_data(withdraw_telephone=message.text)
    await state.set_state()


@router.callback_query(F.data == 'change_withdraw_telephone')
async def change_withdraw_telephone(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(text=replies['withdraw_telephone_reply'])
    await state.set_state(States.INPUT_WITHDRAW_TELEPHONE)


@router.callback_query(F.data == 'confirm_withdraw_telephone')
async def confirm_withdraw_telephone(call: types.CallbackQuery, user: User, state: FSMContext, db_session: AsyncSession) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    data = await state.get_data()
    if not user.bank:
        await call.message.answer(text=replies['withdraw_bank_reply'])
        updated_user = user
        updated_user.telephone = data.get('withdraw_telephone', None)
        db_session.add(updated_user)
        await db_session.commit()
        await state.set_state(States.INPUT_WITHDRAW_BANK)
        return
    else:
        telegram_user_info = '@' + call.from_user.username if call.from_user.username else call.from_user.full_name
        amount = data.get('withdraw_amount')
        record_id = await add_record_to_db(user_id=user.id,
                                           username=telegram_user_info,
                                           operation=OperationType.WITHDRAW,
                                           status=Status.PENDING,
                                           rate=settings.RATE,
                                           coins_amount=amount,
                                           summ=amount * settings.RATE,
                                           db_session=db_session)
        await call.message.answer(text=replies['withdraw_funds_process_сomplete'].format(record_id))
        message = await call.bot.send_message(chat_id=settings.CHAT_ID,
                                              text=replies['new_withdraw_request'].format(record_id,
                                                                                          telegram_user_info,
                                                                                          user.nickname,
                                                                                          data.get('withdraw_telephone'),
                                                                                          user.bank,
                                                                                          amount,
                                                                                          amount * settings.RATE),
                                              reply_markup=get_operation_keyboard(operation=OperationType.WITHDRAW, record_id=record_id))
        record = await get_record_by_id(record_id, db_session)
        record.message_id = message.message_id
        updated_user = user
        updated_user.telephone = data.get('withdraw_telephone')
        db_session.add_all((record, updated_user))
        await db_session.commit()
        await state.set_state()


@router.message(States.INPUT_WITHDRAW_BANK)
async def input_withdraw_bank(message: types.Message, state: FSMContext) -> None:
    await message.answer(text=replies['withdraw_bank_confirmation'].format(message.text),
                         reply_markup=get_confirmation_keyboard(mode=Entities.WITHDRAW_BANK))
    await state.update_data(withdraw_bank=message.text)
    await state.set_state()


@router.callback_query(F.data == 'change_withdraw_bank')
async def change_withdraw_bank(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(text=replies['withdraw_bank_reply'])
    await state.set_state(States.INPUT_WITHDRAW_BANK)


@router.callback_query(F.data == 'confirm_withdraw_bank')
async def confirm_withdraw_bank(call: types.CallbackQuery, user: User, state: FSMContext, db_session: AsyncSession) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    telegram_user_info = '@' + call.from_user.username if call.from_user.username else call.from_user.full_name
    data = await state.get_data()
    amount = data.get('withdraw_amount')
    bank = data.get('withdraw_bank')
    record_id = await add_record_to_db(user_id=user.id,
                                       username=telegram_user_info,
                                       operation=OperationType.WITHDRAW,
                                       status=Status.PENDING,
                                       rate=settings.RATE,
                                       coins_amount=amount,
                                       summ=amount * settings.RATE,
                                       db_session=db_session)
    await call.message.answer(text=replies['withdraw_funds_process_сomplete'].format(record_id))
    message = await call.bot.send_message(chat_id=settings.CHAT_ID,
                                          text=replies['new_withdraw_request'].format(record_id,
                                                                                      telegram_user_info,
                                                                                      user.nickname,
                                                                                      user.telephone,
                                                                                      bank,
                                                                                      amount,
                                                                                      amount * settings.RATE),
                                          reply_markup=get_operation_keyboard(operation=OperationType.WITHDRAW, record_id=record_id))
    updated_user = user
    updated_user.bank = bank
    record = await get_record_by_id(record_id, db_session)
    record.message_id = message.message_id
    db_session.add_all((record, updated_user))
    await db_session.commit()
    await state.set_state()
