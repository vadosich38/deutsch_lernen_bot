from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_ikb() -> InlineKeyboardMarkup:
    my_ikb = InlineKeyboardMarkup(row_width=1)

    confirm_btn = InlineKeyboardButton(text="CONFIRM", callback_data="CONFIRM")
    my_ikb.add(confirm_btn)
    return my_ikb
