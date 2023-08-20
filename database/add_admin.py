import sqlite3 as sq
from database.get_status import is_admin
from database.is_user import is_user
NOW_ADMIN = "Этот пользователь уже является администратором!"
NOT_USER = "Этот пользователь не найден. Сначала он должен запустить бота!"
SUCCESS = "Задание выполнено: пользователь назначен администратором!"
SUPER_ADMIN_SUCCESS = "Задание выполнено: суперадмин назначен администратором!"


def add_admin(db_name: str, date: str, user_id: int, super_admin: bool = False) -> str:
    if not is_user(user_id=user_id):
        return NOT_USER
    elif is_admin(user_id=user_id):
        return NOW_ADMIN

    with sq.connect(db_name) as con:
        cur = con.cursor()

        if super_admin:
            #добавление суперадмина в БД при мервом запуске кода
            cur.execute("""INSERT INTO users VALUES(?, 1, 1, ?)""", (user_id, date, ))
            return SUPER_ADMIN_SUCCESS
        else:
            #добавление обычного администратора
            cur.execute("""UPDATE users SET admin = 1, activ = 1, last_active_date = ? WHERE user_id LIKE(?)""",
                        (date, user_id, ))
            return SUCCESS

