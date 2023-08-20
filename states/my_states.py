from aiogram.dispatcher.filters.state import StatesGroup, State


class MyStatesGroup(StatesGroup):
    verb = State()
    noun = State()
    wait_id_to_add_admin = State()
    wait_id_to_delete_admin = State()
    wait_text_to_send = State()
    choose_photo_regim = State()
    wait_photo_to_send = State()
    confirm_with_photo = State()
