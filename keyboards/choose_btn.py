from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choose_btn_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    with_photo_btn = InlineKeyboardButton(text="WITH BUTTON",
                                          callback_data="WITH BUTTON")
    without_photo_btn = InlineKeyboardButton(text="WITHOUT BUTTON",
                                             callback_data="WITHOUT BUTTON")

    ikb.add(with_photo_btn, without_photo_btn)
    return ikb
