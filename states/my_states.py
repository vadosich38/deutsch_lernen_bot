from aiogram.dispatcher.filters.state import StatesGroup, State


class MyStatesGroup(StatesGroup):
    verb = State()
    noun = State()
