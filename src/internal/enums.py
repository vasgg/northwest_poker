from enum import Enum, StrEnum, auto

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
    DEPOSIT_AMOUNT = auto()
    WITHDRAW_TELEPHONE = auto()
    WITHDRAW_AMOUNT = auto()
    WITHDRAW_BANK = auto()


class SettingsEntities(Enum):
    NICKNAME = auto()
    TELEPHONE = auto()
    BANK = auto()


class Action(Enum):
    CONFIRM = auto()
    REJECT = auto()


class Status(Enum):
    PENDING = auto()
    DONE = auto()
    CANCELED = auto()


class AttachType(Enum):
    DOCUMENT = auto()
    PHOTO = auto()


class OperationType(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()


class Stage(StrEnum):
    DEV = auto()
    PROD = auto()
