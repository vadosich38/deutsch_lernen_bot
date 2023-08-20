from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def choose_photo_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=2)
    with_photo_btn = InlineKeyboardButton(text="WITH PHOTO",
                                          callback_data="WITH PHOTO")
    without_photo_btn = InlineKeyboardButton(text="WITHOUT PHOTO",
                                             callback_data="WITHOUT PHOTO")

    ikb.add(with_photo_btn, without_photo_btn)
    return ikb
