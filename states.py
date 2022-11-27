from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    square = State()
    ears = State()
    image = State()