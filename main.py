from aiogram import executor
from set.dispatcher import my_disp

from handlers.start import cmd_start
from handlers.regims import noun_chang_state, verb_chang_state
from handlers.regims import noun_answer
from handlers.regims import verb_answer
from handlers.callback_preteritum import callback_preteritum
from handlers.callback_presens import callback_presens
from handlers.cmd_add_admin import add_admin
from handlers.cmd_delete_admin import delete_admin
from handlers.cmd_send import cmd_send
from handlers.cmd_send import get_text
from handlers.cmd_send import get_confirm_callback
from handlers.cmd_send import get_photo
from handlers.cmd_send import get_regim_callback
from handlers.cmd_send import confirm_with_photo


from database.create_table import create_db
from database.add_admin import add_admin
from configs.config import ADMIN, db_name
from datetime import datetime


async def on_startup(_):
    create_db(name=db_name)
    print("База данных успешно создана")

    print(add_admin(
        db_name=db_name,
        date=str(datetime.now()),
        user_id=ADMIN,
        super_admin=True))
    print("Бот успешно запущен")


if __name__ == "__main__":
    executor.start_polling(dispatcher=my_disp,
                           on_startup=on_startup,
                           skip_updates=True)
