from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from internal.enums import Action, Entities, OperationType, SettingsEntities


class OperationCallbackFactory(CallbackData, prefix='operation'):
    operation: OperationType
    action: Action
    record_id: int


class SettingsCallbackFactory(CallbackData, prefix='settings'):
    entity: SettingsEntities


class SettingsConfirmationCallbackFactory(CallbackData, prefix='info'):
    entity: SettingsEntities
    attr: str
    payload: str


def get_info_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🪪 изменить ник', callback_data=SettingsCallbackFactory(
                    entity=SettingsEntities.NICKNAME
                ).pack())
            ],
            [
                InlineKeyboardButton(text='📞 изменить телефон', callback_data=SettingsCallbackFactory(
                    entity=SettingsEntities.TELEPHONE
                ).pack())
            ],
            [
                InlineKeyboardButton(text='🏦 изменить банк', callback_data=SettingsCallbackFactory(
                    entity=SettingsEntities.BANK
                ).pack())
            ],
        ],
    )


def get_info_confirmation_keyboard(entity: SettingsEntities, text: str, payload: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ подтвердить ' + text, callback_data=SettingsConfirmationCallbackFactory(
                    entity=entity,
                    attr='confirm_' + text,
                    payload=payload,
                ).pack())
            ],
            [
                InlineKeyboardButton(text='🔄 изменить ' + text, callback_data=SettingsConfirmationCallbackFactory(
                    entity=entity,
                    attr='change_' + text,
                    payload=payload,
                ).pack())
            ],
        ],
    )


def get_operation_keyboard(operation: OperationType, record_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ ' + Action.CONFIRM.value + ' ' + operation.value, callback_data=OperationCallbackFactory(
                    operation=operation,
                    action=Action.CONFIRM,
                    record_id=record_id,
                ).pack()),
            ],
            [
                InlineKeyboardButton(text='❌ ' + Action.REJECT.value + ' ' + operation.value, callback_data=OperationCallbackFactory(
                    operation=operation,
                    action=Action.REJECT,
                    record_id=record_id,
                ).pack()),
            ],
        ],
    )


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
        case Entities.DEPOSIT_AMOUNT:
            confirm_data = 'confirm_deposit_amount'
            change_data = 'change_deposit_amount'
        case Entities.WITHDRAW_AMOUNT:
            confirm_data = 'confirm_withdraw_amount'
            change_data = 'change_withdraw_amount'
        case Entities.WITHDRAW_TELEPHONE:
            confirm_data = 'confirm_withdraw_telephone'
            change_data = 'change_withdraw_telephone'
        case Entities.WITHDRAW_BANK:
            confirm_data = 'confirm_withdraw_bank'
            change_data = 'change_withdraw_bank'
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
