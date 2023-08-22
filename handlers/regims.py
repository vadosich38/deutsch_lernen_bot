from aiogram import types
from states.my_states import MyStatesGroup
from set.dispatcher import my_disp, my_bot
from configs.config import LETTERS_PARS, VERB_LINK, ENDEN, NOUN_LINK
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import InvalidHTTPUrlContent
from keyboards.ikb import inline_kb
import requests
from aiogram.dispatcher.filters import Text


@my_disp.message_handler(Text(equals="Хочу узнать больше о глаголах  🧠", ignore_case=True),
                         state="*")
async def verb_chang_state(message: types.Message, state: FSMContext):
    if state == MyStatesGroup.verb:
        await message.reply("Бот уже работает в этом режиме!  🛑")
    else:
        await MyStatesGroup.verb.set()
        await message.reply("Теперь отправь мне любой глагол на немецком языке  🇩🇪")


@my_disp.message_handler(Text(equals="Хочу узнать больше о существительных  💪", ignore_case=True),
                         state="*")
async def noun_chang_state(message: types.Message, state: FSMContext):
    if state == MyStatesGroup.noun:
        await message.reply("Бот уже работает в этом режиме!  🛑")
    else:
        await MyStatesGroup.noun.set()
        await message.reply("Теперь отправь мне любое существительное на немецком языке  🇩🇪")


@my_disp.message_handler(lambda message: not message.text.startswith("/"),
                         state=MyStatesGroup.verb)
async def verb_answer(message: types.Message, state: FSMContext) -> None:
    wort = message.text.lower()
    for letter, umlaut in LETTERS_PARS.items():
        if umlaut in wort:
            wort = wort.replace(umlaut, letter + "3")

    for i_ende in ENDEN:
        wort_link = VERB_LINK + wort + i_ende
        response = requests.get(url=wort_link)
        if response.status_code != 404:
            async with state.proxy() as data:
                data["wort"] = wort
                data["message"] = message
                data["wort_link"] = wort_link
            await my_bot.send_photo(chat_id=message.chat.id,
                                    photo=wort_link,
                                    caption="Вот ваш глагол  👨🏻‍🏫",
                                    reply_markup=inline_kb())
            break

    else:
        await message.reply(text="Такой глагол не найден  👮‍♂️")


@my_disp.message_handler(lambda message: not message.text.startswith("/"),
                         state=MyStatesGroup.noun)
async def noun_answer(message: types.Message) -> None:
    wort = message.text.capitalize()
    for letter, umlaut in LETTERS_PARS.items():
        if umlaut in wort:
            wort = wort.replace(umlaut, letter + "3")

    wort_link = NOUN_LINK + wort + ".png"
    try:
        await my_bot.send_photo(chat_id=message.chat.id,
                                photo=wort_link,
                                caption="Вот ваше существительное  👨🏻‍🏫")
    except InvalidHTTPUrlContent:
        await message.reply(text="Такое существительно не найдено  👮‍♂️")
