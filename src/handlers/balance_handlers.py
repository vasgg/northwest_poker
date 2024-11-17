from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database.crud.record import get_record_by_id
from database.crud.user import add_record_to_db
from database.models.user import User
from internal.enums import AttachType, Entities, OperationType, States, Status
from internal.texts import replies
from internal.keyboards import get_confirmation_keyboard, get_operation_keyboard

router = Router()
media_filter = F.photo | F.document


@router.message(States.INPUT_DEPOSIT_AMOUNT)
async def input_amount(message: types.Message, state: FSMContext) -> None:
    try:
        amount = int(message.text)
        await message.answer(text=replies['add_funds_сonfirmation'].format(amount, amount * settings.RATE),
                             reply_markup=get_confirmation_keyboard(mode=Entities.DEPOSIT_AMOUNT))
        await state.update_data(deposit_amount=amount)
        await state.set_state()
    except ValueError:
        await message.answer(text=replies['add_funds_error_reply'].format(settings.RATE))
        return


@router.callback_query(F.data == 'change_deposit_amount')
async def change_amount(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(text=replies['add_funds_reply'].format(settings.RATE))
    await state.set_state(States.INPUT_DEPOSIT_AMOUNT)


@router.callback_query(F.data == 'confirm_deposit_amount')
async def confirm_amount(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    data = await state.get_data()
    await call.message.answer(text=replies['add_funds_requisites'].format(
        data['deposit_amount'] * settings.RATE, settings.TELEPHONE.get_secret_value()))
    await state.set_state(States.INPUT_SCREENSHOT)


@router.message(media_filter)
@router.message(States.INPUT_SCREENSHOT)
async def input_media(message: types.Message, state: FSMContext, user: User, db_session: AsyncSession) -> None:
    telegram_user_info = '@' + message.from_user.username if user.username else message.from_user.full_name
    data = await state.get_data()
    if message.photo:
        docunent_id = message.photo[-1].file_id
        attach_type = AttachType.PHOTO
    elif message.document:
        docunent_id = message.document.file_id
        attach_type = AttachType.DOCUMENT
    else:
        return
    try:
        amount = data['deposit_amount']
    except KeyError:
        await message.answer(text=replies['error_reply'])
        return
    record_id = await add_record_to_db(user_id=user.id,
                                       username=telegram_user_info,
                                       operation=OperationType.DEPOSIT,
                                       status=Status.PENDING,
                                       rate=settings.RATE,
                                       coins_amount=amount,
                                       summ=amount * settings.RATE,
                                       attach_type=attach_type,
                                       attach_id=docunent_id,
                                       db_session=db_session)
    await message.answer(text=replies['add_funds_process_сomplete'].format(record_id))
    if attach_type == AttachType.PHOTO:
        await message.bot.send_photo(chat_id=settings.CHAT_ID,
                                     photo=docunent_id,
                                     caption=f'изображение к заявке {record_id}')
    else:
        await message.bot.send_document(chat_id=settings.CHAT_ID,
                                        document=docunent_id,
                                        caption=f'документ к заявке {record_id}')
    message = await message.bot.send_message(chat_id=settings.CHAT_ID,
                                             text=replies['new_deposit_request'].format(record_id,
                                                                                        telegram_user_info,
                                                                                        user.nickname,
                                                                                        amount,
                                                                                        amount * settings.RATE),
                                             reply_markup=get_operation_keyboard(operation=OperationType.DEPOSIT, record_id=record_id))
    record = await get_record_by_id(record_id, db_session)
    record.message_id = message.message_id
    db_session.add(record)
    await db_session.commit()
    await state.set_state()


@router.message(States.INPUT_WITHDRAW_AMOUNT)
async def input_withdraw_amount(message: types.Message, state: FSMContext) -> None:
    try:
        amount = int(message.text)
        await message.answer(text=replies['withdraw_funds_сonfirmation'].format(amount, amount * settings.RATE),
                             reply_markup=get_confirmation_keyboard(mode=Entities.WITHDRAW_AMOUNT))
        await state.update_data(withdraw_amount=amount)
        await state.set_state()
    except ValueError:
        await message.answer(text=replies['withdraw_funds_error_reply'].format(settings.RATE))
        return


@router.callback_query(F.data == 'change_withdraw_amount')
async def change_withdraw_amount(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    await call.message.answer(text=replies['withdraw_funds_reply'].format(settings.RATE))
    await state.set_state(States.INPUT_WITHDRAW_AMOUNT)


@router.callback_query(F.data == 'confirm_withdraw_amount')
async def confirm_withdraw_amount(call: types.CallbackQuery, user: User, state: FSMContext, db_session: AsyncSession) -> None:
    await call.answer()
    await call.message.edit_reply_markup()
    if not user.telephone:
        await call.message.answer(text=replies['withdraw_telephone_reply'])
        await state.set_state(States.INPUT_WITHDRAW_TELEPHONE)
        return
    else:
        if not user.bank:
            await call.message.answer(text=replies['withdraw_bank_reply'])
            await state.set_state(States.INPUT_WITHDRAW_BANK)
            return
        else:
            telegram_user_info = '@' + call.from_user.username if call.from_user.username else call.from_user.full_name
            data = await state.get_data()
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
                                                                                              user.telephone,
                                                                                              user.bank,
                                                                                              amount,
                                                                                              amount * settings.RATE),
                                                  reply_markup=get_operation_keyboard(operation=OperationType.WITHDRAW, record_id=record_id))
            record = await get_record_by_id(record_id, db_session)
            record.message_id = message.message_id
            db_session.add(record)
            await db_session.commit()
            await state.set_state()
