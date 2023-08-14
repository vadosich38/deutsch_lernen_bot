from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def regular_kb() -> ReplyKeyboardMarkup:
    my_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    verb_button = KeyboardButton(text="Хочу узнать больше о глаголах  🧠")
    noun_button = KeyboardButton(text="Хочу узнать больше о существительных  💪")

    my_kb.add(verb_button, noun_button)
    return my_kb
