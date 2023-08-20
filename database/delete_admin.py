import sqlite3 as sq
from configs.config import db_name, ADMIN
from .is_user import is_user
from .get_status import is_admin

NO_USER = "Такой пользователь не найден!"
NOT_ADMIN = "Этот пользователь не является администратором"
SUPER_ADMIN = "Этого пользователя нельзя разжаловать"
SUCCESS = "Задание выполнено: пользователь больше не администратор"


def delete_admin(user_id: int) -> str:
    if not is_user(user_id=user_id):
        return NO_USER
    if not is_admin(user_id=user_id):
        return NOT_ADMIN

    del_process(user_id=user_id)
    return SUCCESS


def del_process(user_id: int):
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("""UPDATE users SET admin = 0 WHERE user_id LIKE(?)""", (user_id,))





    # if is_user(user_id=user_id):
    #     if is_admin(user_id=user_id):
    #         with sq.connect(db_name) as con:
    #             cur = con.cursor()
    #             cur.execute("""UPDATE users SET admin = 0 WHERE user_id LIKE(?)""", (user_id,))
    #             return SUCCESS
    #
    #     return NOT_ADMIN
    #
    # return NO_USER



    #
    # with sq.connect(db_name) as con:
    #     cur = con.cursor()
    #
    #     if user_id == ADMIN:
    #         return SUPER_ADMIN
    #
    #     cur.execute("""SELECT admin FROM users WHERE user_id LIKE(?)""", (user_id,))
    #     result = cur.fetchone()
    #
    #     if not result:
    #         return NO_USER
    #
    #     if result[0] == 1:
    #         cur.execute("""UPDATE users SET admin = 0 WHERE user_id LIKE(?)""", (user_id,))
    #         return SUCCESS
    #     else:
    #         return NOT_ADMIN
