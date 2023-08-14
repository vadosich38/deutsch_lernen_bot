from set.dispatcher import my_disp, my_bot
from states.my_states import MyStatesGroup
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from configs.config import VERB_LINK, PRESENS_LINK
from aiogram.utils.exceptions import InvalidHTTPUrlContent


@my_disp.callback_query_handler(text="presens", state=MyStatesGroup.verb)
async def callback_presens(callback_data: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        message = data["message"]
        wort_link = data["wort_link"].replace(VERB_LINK, "")
        wort_link = PRESENS_LINK + wort_link
    print(wort_link)

    await callback_data.answer(text="Будет выполнено  🫡")

    try:
        await my_bot.send_photo(chat_id=message.chat.id,
                                photo=wort_link,
                                caption="Этот глагол в Präsens  👨🏻‍🏫")
    except InvalidHTTPUrlContent:
        await message.reply(text="Для этого глагола данные не найдены  👮‍♂️")
