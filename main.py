from aiogram import executor
from set.dispatcher import my_disp
from database.db_class import Database
from configs.config import db_connection
from configs.config import ADMIN
from datetime import datetime

from handlers.start import cmd_start
from handlers.regims import noun_chang_state, verb_chang_state
from handlers.callback_preteritum import callback_preteritum
from handlers.callback_presens import callback_presens
from handlers.cmd_add_admin import cmd_add_admin
from handlers.cmd_delete_admin import cmd_delete_admin
from handlers.cmd_send import cmd_send
from handlers.cmd_send import get_text
from handlers.cmd_send import get_confirm_callback
from handlers.cmd_send import get_photo
from handlers.cmd_send import get_regim_callback
from handlers.cmd_send import confirm_with_photo
from handlers.regims import noun_answer
from handlers.regims import verb_answer


async def on_startup(_):
    Database.create_table(conn=db_connection)
    print("База данных успешно создана")

    print(Database.add_admin(
        date=str(datetime.now()),
        user_id=ADMIN,
        super_admin=True,
        conn=db_connection))
    print("Бот успешно запущен")


if __name__ == "__main__":
    try:
        executor.start_polling(dispatcher=my_disp,
                               on_startup=on_startup,
                               skip_updates=True)
    except Exception as error_name:
        print("Возникла ошибка:", error_name)
    finally:
        db_connection.commit()
        db_connection.close()
