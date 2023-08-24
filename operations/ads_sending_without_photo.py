from set.bot import my_bot
from aiogram.utils.exceptions import BotBlocked
from database.db_class import Database
from datetime import datetime
from configs.config import db_connection


async def sending_without_photo(author_id: int, text: str, regim: str) -> None:
    users_list = Database.get_users(regim=regim, conn=db_connection)
    success = 0
    failed = 0

    for i_user_id in users_list:
        try:
            await my_bot.send_message(chat_id=i_user_id[0],
                                      text=text)
            success += 1
            Database.update_activ_date(user_id=i_user_id[0],
                                       date=str(datetime.now()),
                                       conn=db_connection)
        except BotBlocked as ex:
            print("При рассылке возникла ошибка: ", ex)
            failed += 1
            Database.update_activ_status(user_id=i_user_id[0],
                                         conn=db_connection)
    else:
        await my_bot.send_message(chat_id=author_id,
                                  text="Рассылка выполнена! Успешно отправлено {} сообщений\n"
                                       "Не доставлено {} сообщений".format(success, failed))
