from set.dispatcher import my_disp
from set.bot import my_bot
from aiogram import types
from configs.config import ADMIN, db_connection
from states.my_states import MyStatesGroup
from aiogram.dispatcher import FSMContext
from database.db_class import Database

NOT_ADMIN = "Разжаловать администратора может только администратор. Вы не администратор!"
ID_ISNT_CORRECT = "Этот ID не корректен, попробуйте еще раз. Длина ID должна составлять 9 или 10 символов"
CANCELLING = "Вы отменили удаление администратора!"
INSTRUCTION = "Теперь пришлите Telegram ID пользователя, которого нужно разжаловать"


@my_disp.message_handler(commands=["delete_admin"],
                         state="*")
async def cmd_delete_admin(message: types.Message):
    if ADMIN == message.from_user.id or Database.is_admin(user_id=message.from_user.id, conn=db_connection):
        await MyStatesGroup.wait_id_to_delete_admin.set()
        await message.reply(text=INSTRUCTION)
    else:
        await message.reply(text=NOT_ADMIN)


@my_disp.message_handler(commands=["cancel"], state=MyStatesGroup.wait_id_to_delete_admin)
async def cancel_admin_adding(message: types.Message, state: FSMContext):
    await message.reply(text=CANCELLING)
    await state.finish()


@my_disp.message_handler(lambda message: message.text,
                         state=MyStatesGroup.wait_id_to_delete_admin)
async def get_id_to_delete_admin(message: types.Message, state: FSMContext):
    if 9 <= len(message.text) <= 10:
        answer = Database.delete_admin(user_id=int(message.text), conn=db_connection)
        if answer == Database.SUCCESS_DEL:
            await state.finish()
            await my_bot.send_message(chat_id=message.text,
                                      text="Вы больше не администратор бота!")

        await message.reply(text=answer)

    else:
        await message.reply(text=ID_ISNT_CORRECT)
