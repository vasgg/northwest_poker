from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.config import settings
from src.database.crud.user import add_record_to_db
from src.database.models.user import User
from src.enums import Entities, States
from src.internal.blink1 import blink1_yellow
from src.internal.texts import replies
from src.keyboards import get_confirmation_keyboard

router = Router()


@router.message(States.INPUT_AMOUNT)
async def input_amount(message: types.Message, state: FSMContext) -> None:
    try:
        amount = int(message.text)
        await message.answer(text=replies['add_funds_сonfirmation'].format(amount, amount * settings.RATE),
                             reply_markup=get_confirmation_keyboard(mode=Entities.AMOUNT))
        await state.update_data(amount=amount)
        await state.set_state()
    except ValueError:
        await message.answer(text=replies['add_funds_error_reply'])
        return


@router.callback_query(F.data == 'confirm_amount')
async def confirm_amount(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    data = await state.get_data()
    await call.message.answer(text=replies['add_funds_requisites'].format(data['amount'] * settings.RATE, settings.TELEPHONE.get_secret_value()))
    await state.set_state(States.INPUT_SCREENSHOT)


@router.callback_query(F.data == 'change_amount')
async def change_amount(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.answer(text=replies['add_funds_reply'])
    await state.set_state(States.INPUT_AMOUNT)


@router.message(F.photo)
@router.message(States.INPUT_SCREENSHOT)
async def input_screenshot(message: types.Message, state: FSMContext, user: User, db_session) -> None:
    telegram_user_info = '@' + message.from_user.username if user.username else message.from_user.full_name
    data = await state.get_data()
    image_id = message.photo[-1].file_id
    amount = data['amount']
    await message.answer(text=replies['add_funds_process_сomplete'])
    record_id = await add_record_to_db(user_id=user.id,
                                       username=telegram_user_info,
                                       rate=settings.RATE,
                                       coins_amount=amount,
                                       summ=amount * settings.RATE,
                                       image_id=image_id,
                                       db_session=db_session)
    await blink1_yellow()
    await message.bot.send_photo(chat_id=settings.CHAT_ID,
                                 photo=image_id,
                                 caption=replies['new_request'].format(record_id,
                                                                       telegram_user_info,
                                                                       user.nickname,
                                                                       amount,
                                                                       amount * settings.RATE))
    await state.set_state()
