from enum import Enum

from aiogram.filters.state import State, StatesGroup


class States(StatesGroup):
    INPUT_NICK = State()
    INPUT_DEPOSIT_AMOUNT = State()
    INPUT_WITHDRAW_AMOUNT = State()
    INPUT_WITHDRAW_TELEPHONE = State()
    INPUT_WITHDRAW_BANK = State()
    INPUT_SCREENSHOT = State()


class SettingsStates(StatesGroup):
    INPUT_NICKNAME = State()
    INPUT_TELEPHONE = State()
    INPUT_BANK = State()


class Entities(Enum):
    NICK = 'nick'
    DEPOSIT_AMOUNT = 'deposit_amount'
    WITHDRAW_TELEPHONE = 'withdraw_telephone'
    WITHDRAW_AMOUNT = 'withdraw_amount'
    WITHDRAW_BANK = 'withdraw_bank'


class SettingsEntities(Enum):
    NICKNAME = 'nickname'
    TELEPHONE = 'telephone'
    BANK = 'bank'


class Action(Enum):
    CONFIRM = 'confirm'
    REJECT = 'reject'


class Status(Enum):
    PENDING = 'pending'
    DONE = 'done'
    CANCELED = 'canceled'


class AttachType(Enum):
    DOCUMENT = 'document'
    PHOTO = 'photo'


class OperationType(Enum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
