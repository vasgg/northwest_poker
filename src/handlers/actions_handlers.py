from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database.crud.record import get_record_by_id
from database.crud.user import get_user_by_id
from database.models.user import User
from internal.enums import Action, OperationType, SettingsEntities, SettingsStates, Status
from internal.keyboards import OperationCallbackFactory, SettingsCallbackFactory, SettingsConfirmationCallbackFactory, get_info_confirmation_keyboard
from internal.texts import replies

router = Router()


@router.callback_query(OperationCallbackFactory.filter())
async def action_button_processing(
        callback: types.CallbackQuery,
        callback_data: OperationCallbackFactory,
        state: FSMContext,
        db_session: AsyncSession,
) -> None:
    await callback.answer()
    if callback.from_user.id not in settings.ADMINS:
        await callback.message.answer(text=replies['administration_reply'])
        return
    operation = callback_data.operation
    action = callback_data.action
    record_id = callback_data.record_id
    record = await get_record_by_id(record_id, db_session)
    record.operation = operation
    record.status = Status.DONE if action == Action.CONFIRM else Status.CANCELED
    user_for_reply = await get_user_by_id(record.user_id, db_session)
    telegram_user_info = '@' + user_for_reply.username if user_for_reply.username else (
            user_for_reply.first_name + ' ' + user_for_reply.last_name) if user_for_reply.last_name else user_for_reply.first_name
    match operation, action:
        case OperationType.DEPOSIT, Action.CONFIRM:
            text = ('✅ Заявка на депозит выполнена ✅ \n\n'
                    + replies['new_deposit_request'].format(record.id,
                                                            telegram_user_info,
                                                            user_for_reply.nickname,
                                                            record.coins_amount,
                                                            record.coins_amount * settings.RATE))
        case OperationType.WITHDRAW, Action.CONFIRM:
            text = ('✅ Заявка на вывод выполнена ✅ \n\n'
                    + replies['new_withdraw_request'].format(record.id,
                                                             telegram_user_info,
                                                             user_for_reply.nickname,
                                                             user_for_reply.telephone,
                                                             user_for_reply.bank,
                                                             record.coins_amount,
                                                             record.coins_amount * settings.RATE))
        case OperationType.DEPOSIT, Action.REJECT:
            text = ('❌ Заявка на депозит отклонена ❌ \n\n'
                    + replies['new_deposit_request'].format(record.id,
                                                            telegram_user_info,
                                                            user_for_reply.nickname,
                                                            record.coins_amount,
                                                            record.coins_amount * settings.RATE))
        case OperationType.WITHDRAW, Action.REJECT:
            text = ('❌ Заявка на вывод отклонена ❌ \n\n'
                    + replies['new_withdraw_request'].format(record.id,
                                                             telegram_user_info,
                                                             user_for_reply.nickname,
                                                             user_for_reply.telephone,
                                                             user_for_reply.bank,
                                                             record.coins_amount,
                                                             record.coins_amount * settings.RATE))
        case _:
            assert False, "Unexpected combination"

    await callback.bot.edit_message_text(chat_id=settings.CHAT_ID,
                                         message_id=record.message_id,
                                         text=text)
    db_session.add(record)
    await db_session.commit()
    reply_message = replies['action_confirm_report'].format(record_id) if action == Action.CONFIRM \
        else replies['action_reject_report'].format(record_id)
    await callback.bot.send_message(chat_id=user_for_reply.telegram_id, text=reply_message)
    await state.clear()


@router.callback_query(SettingsCallbackFactory.filter())
async def info_button_processing(
        callback: types.CallbackQuery,
        callback_data: SettingsCallbackFactory,
        state: FSMContext,
) -> None:
    await callback.answer()
    await callback.message.edit_reply_markup()
    entity = callback_data.entity
    match entity:
        case SettingsEntities.NICKNAME:
            await callback.message.answer(text=replies['registration_nick'])
            await state.set_state(SettingsStates.INPUT_NICKNAME)
            await state.update_data(registration_entity=entity)
        case SettingsEntities.TELEPHONE:
            await callback.message.answer(text=replies['withdraw_telephone_reply'])
            await state.set_state(SettingsStates.INPUT_TELEPHONE)
        case SettingsEntities.BANK:
            await callback.message.answer(text=replies['withdraw_bank_reply'])
            await state.set_state(SettingsStates.INPUT_BANK)
        case _:
            assert False, "Unexpected entity"


@router.message(SettingsStates.INPUT_NICKNAME)
@router.message(SettingsStates.INPUT_TELEPHONE)
@router.message(SettingsStates.INPUT_BANK)
async def input_settings_entity(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    match current_state:
        case SettingsStates.INPUT_NICKNAME:
            await message.answer(text=replies['registration_nick_confirmation'].format(message.text),
                                 reply_markup=get_info_confirmation_keyboard(SettingsEntities.NICKNAME, 'ник', message.text))
        case SettingsStates.INPUT_TELEPHONE:
            await message.answer(text=replies['withdraw_telephone_confirmation'].format(message.text),
                                 reply_markup=get_info_confirmation_keyboard(SettingsEntities.TELEPHONE, 'телефон', message.text))
        case SettingsStates.INPUT_BANK:
            await message.answer(text=replies['withdraw_bank_confirmation'].format(message.text),
                                 reply_markup=get_info_confirmation_keyboard(SettingsEntities.BANK, 'банк', message.text))
        case _:
            assert False, "Unexpected state"


@router.callback_query(SettingsConfirmationCallbackFactory.filter())
async def change_user_info(callback: types.CallbackQuery,
                           callback_data: SettingsConfirmationCallbackFactory,
                           user: User,
                           state: FSMContext,
                           db_session: AsyncSession) -> None:
    await callback.answer()
    await callback.message.edit_reply_markup()
    entity = callback_data.entity
    attr = callback_data.attr
    payload = callback_data.payload
    updated_user = user
    match entity, attr:
        case SettingsEntities.NICKNAME, 'confirm_ник':
            await callback.message.answer(text=replies['nick_changed'].format(payload))
            await state.set_state()
            updated_user.nickname = payload
        case SettingsEntities.NICKNAME, 'change_ник':
            await callback.message.answer(text=replies['registration_nick'])
            await state.set_state(SettingsStates.INPUT_NICKNAME)
        case SettingsEntities.TELEPHONE, 'confirm_телефон':
            await callback.message.answer(text=replies['telephone_changed'].format(payload))
            await state.set_state()
            updated_user.telephone = payload
        case SettingsEntities.TELEPHONE, 'change_телефон':
            await callback.message.answer(text=replies['withdraw_telephone_reply'])
            await state.set_state(SettingsStates.INPUT_TELEPHONE)
        case SettingsEntities.BANK, 'confirm_банк':
            await callback.message.answer(text=replies['bank_changed'].format(payload))
            await state.set_state()
            updated_user.bank = payload
        case SettingsEntities.BANK, 'change_банк':
            await callback.message.answer(text=replies['withdraw_bank_reply'])
            await state.set_state(SettingsStates.INPUT_BANK)
        case _:
            print(entity, attr)
            assert False, "Unexpected combination"
    db_session.add(updated_user)
    await db_session.commit()
