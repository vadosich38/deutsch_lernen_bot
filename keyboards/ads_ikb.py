from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ads_ikb(btn_text: str, btn_link: str) -> InlineKeyboardMarkup:
    my_ikb = InlineKeyboardMarkup(row_width=1)

    ads_btn = InlineKeyboardButton(text=btn_text, url=btn_link)
    my_ikb.add(ads_btn)
    return my_ikb
