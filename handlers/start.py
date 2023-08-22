from set.dispatcher import my_disp
from aiogram import types
from keyboards.kb import regular_kb
from configs.config import START_TEXT, db_name
from datetime import datetime
from database.db_class import Database


@my_disp.message_handler(commands=["start"], state="*")
async def cmd_start(message: types.Message) -> None:
    await message.delete()
    await message.answer(text=START_TEXT,
                         reply_markup=regular_kb())
    Database.new_user_create(user_id=message.from_user.id,
                             date=str(datetime.now()),
                             db_name=db_name)

