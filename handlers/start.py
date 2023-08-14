from set.dispatcher import my_disp
from aiogram import types
from keyboards.kb import regular_kb
from configs.config import START_TEXT


@my_disp.message_handler(commands=["start"], state="*")
async def cmd_start(message: types.Message) -> None:
    await message.delete()
    await message.answer(text=START_TEXT,
                         reply_markup=regular_kb())
