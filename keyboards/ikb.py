from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def inline_kb() -> InlineKeyboardMarkup:
    my_ikb = InlineKeyboardMarkup(row_width=3)
    pr_button = InlineKeyboardButton(text="Präteritum  👀",
                                     callback_data="preteritum")
    presens_button = InlineKeyboardButton(text="Präsens  👀",
                                          callback_data="presens")
    my_ikb.add(pr_button, presens_button)

    return my_ikb
