from enum import Enum

from aiogram.filters.state import State, StatesGroup


class States(StatesGroup):
    INPUT_NICK = State()
    INPUT_AMOUNT = State()
    INPUT_SCREENSHOT = State()


class Entities(Enum):
    NICK = 'nick'
    AMOUNT = 'amount'


class Status(Enum):
    PENDING = 'pending'
    DONE = 'done'
    CANCELED = 'canceled'
