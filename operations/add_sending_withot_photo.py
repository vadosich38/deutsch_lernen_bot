from set.bot import my_bot
from database.return_users import get_users
from aiogram.utils.exceptions import BotBlocked
from database.update_activ_status import update_activ_status
from database.update_activ_date import update_activ_date
from datetime import datetime


async def sending_without_photo(author_id: int, text: str, regim: str) -> None:
    users_list = get_users(regim=regim)
    success = 0
    failed = 0

    for i_user_id in users_list:
        try:
            await my_bot.send_message(chat_id=i_user_id[0],
                                      text=text)
            success += 1
            update_activ_date(user_id=i_user_id[0],
                              date=str(datetime.now()))
        except BotBlocked as ex:
            print("При рассылке возникла ошибка: ", ex)
            failed += 1
            update_activ_status(user_id=i_user_id[0])
    else:
        await my_bot.send_message(chat_id=author_id,
                                  text="Рассылка выполнена! Успешно отправлено {} сообщений\n"
                                       "Не доставлено {} сообщений".format(success, failed))
