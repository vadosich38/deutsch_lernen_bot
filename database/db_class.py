import sqlite3 as sq

import configs.config


class Database:
    NOW_ADMIN = "Этот пользователь уже является администратором!"
    NOT_ADMIN = "Этот пользователь не является администратором!"
    SUPER_ADMIN = "Этого пользователя нельзя разжаловать!"
    SUPER_ADMIN_SUCCESS = "Задание выполнено: суперадмин назначен администратором!"
    SUCCESS_DEL = "Задание выполнено: пользователь больше не администратор"
    SUCCESS_ADD = "Задание выполнено: пользователь назначен администратором!"
    NOT_USER = "Такой пользователь не найден. Сначала он должен запустить бота!"

    @classmethod
    def create_table(cls, db_name: str) -> None:
        with sq.connect(db_name) as con:
            cur = con.cursor()

            # cur.execute("""DROP TABLE IF EXISTS users""")

            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                user_id INTEGER,
                                admin INTEGER,
                                activ INTEGER,
                                last_active_date TEXT)""")

    @classmethod
    def new_user_create(cls, user_id: int, date: str, db_name: str) -> None:
        if not cls.is_user(user_id=user_id, db_name=db_name):
            with sq.connect(db_name) as con:
                cur = con.cursor()
                cur.execute("""INSERT INTO users VALUES(?, ?, ?, ?)""", (user_id, 0, 1, date,))

    @classmethod
    def add_admin(cls, db_name: str, date: str, user_id: int, super_admin: bool = False) -> str:
        if not cls.is_user(user_id=user_id, db_name=db_name):
            return cls.NOT_USER
        elif cls.is_admin(user_id=user_id, db_name=db_name):
            return cls.NOW_ADMIN

        with sq.connect(db_name) as con:
            cur = con.cursor()

            if super_admin:
                # добавление суперадмина в БД при мервом запуске кода
                cur.execute("""INSERT INTO users VALUES(?, 1, 1, ?)""", (user_id, date,))
                return cls.SUPER_ADMIN_SUCCESS
            else:
                # добавление обычного администратора
                cur.execute("""UPDATE users SET admin = 1, activ = 1, last_active_date = ? WHERE user_id LIKE(?)""",
                            (date, user_id,))
                return cls.SUCCESS_ADD

    @classmethod
    def delete_admin(cls, user_id: int, db_name: str) -> str:
        if not cls.is_user(user_id=user_id, db_name=db_name):
            return cls.NOT_USER
        if not cls.is_admin(user_id=user_id, db_name=db_name):
            return cls.NOT_ADMIN

        cls.delete_process(user_id=user_id, db_name=configs.config.db_name)
        return cls.SUCCESS_DEL

    @classmethod
    def delete_process(cls, user_id: int, db_name: str):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute("""UPDATE users SET admin = 0 WHERE user_id LIKE(?)""", (user_id,))

    @classmethod
    def is_user(cls, user_id: int, db_name: str) -> bool:
        with sq.connect(db_name) as con:
            cur = con.cursor()

            res = cur.execute("""SELECT activ FROM users WHERE user_id LIKE(?)""", (user_id,))
            if res.fetchone():
                return True
            else:
                return False

    @classmethod
    def is_admin(cls, user_id: int, db_name: str) -> bool:
        with sq.connect(db_name) as con:
            cur = con.cursor()

            res = cur.execute("""SELECT admin FROM users WHERE user_id LIKE(?)""", (user_id,)).fetchone()

            if res and res[0] == 1:
                return True
            else:
                return False

    @classmethod
    def get_users(cls, db_name: str, regim: str = "all") -> list:
        with sq.connect(db_name) as con:
            cur = con.cursor()

            if regim == "all":
                ids_list = cur.execute("""SELECT user_id FROM users""").fetchall()
                return ids_list
            if regim == "activ":
                ids_list = cur.execute("""SELECT user_id FROM users WHERE activ == 1""").fetchall()
                return ids_list

    @classmethod
    def update_activ_date(cls, user_id: int, date: str, db_name: str) -> None:
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET activ = 1, last_active_date = ? WHERE user_id = ?", (date, user_id))

    @classmethod
    def update_activ_status(cls, user_id: int, db_name: str) -> None:
        with sq.connect(db_name) as con:
            cur = con.cursor()

            cur.execute("""UPDATE users SET activ = 0 WHERE user_id LIKE(?)""", (user_id, ))
