import sqlite3 as sq


class Database:
    NOW_ADMIN = "Этот пользователь уже является администратором!"
    NOT_ADMIN = "Этот пользователь не является администратором!"
    SUPER_ADMIN = "Этого пользователя нельзя разжаловать!"
    SUPER_ADMIN_SUCCESS = "Задание выполнено: суперадмин назначен администратором!"
    SUCCESS_DEL = "Задание выполнено: пользователь больше не администратор"
    SUCCESS_ADD = "Задание выполнено: пользователь назначен администратором!"
    NOT_USER = "Такой пользователь не найден. Сначала он должен запустить бота!"

    @staticmethod
    def create_table(conn: sq.Connection) -> None:
        cur = conn.cursor()
        # cur.execute("""DROP TABLE IF EXISTS users""")

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                            user_id INTEGER,
                            admin INTEGER,
                            activ INTEGER,
                            last_active_date TEXT)""")
        conn.commit()

    @classmethod
    def new_user_create(cls, user_id: int, date: str, conn: sq.Connection) -> None:
        cur = conn.cursor()

        if not cls.is_user(user_id=user_id, conn=conn):
            cur.execute("""INSERT INTO users VALUES(?, ?, ?, ?)""", (user_id, 0, 1, date,))
            conn.commit()

    @classmethod
    def add_admin(cls, conn: sq.Connection, date: str, user_id: int, super_admin: bool = False) -> str:
        cur = conn.cursor()

        if not cls.is_user(user_id=user_id, conn=conn):
            return cls.NOT_USER
        elif cls.is_admin(user_id=user_id, conn=conn):
            return cls.NOW_ADMIN

        if super_admin:
            # добавление суперадмина в БД при мервом запуске кода
            cur.execute("""INSERT INTO users VALUES(?, 1, 1, ?)""", (user_id, date,))
            conn.commit()
            return cls.SUPER_ADMIN_SUCCESS
        else:
            # добавление обычного администратора
            cur.execute("""UPDATE users SET admin = 1, activ = 1, last_active_date = ? WHERE user_id LIKE(?)""",
                        (date, user_id,))
            conn.commit()
            return cls.SUCCESS_ADD

    @classmethod
    def delete_admin(cls, user_id: int, conn: sq.Connection) -> str:
        if not cls.is_user(user_id=user_id, conn=conn):
            return cls.NOT_USER
        if not cls.is_admin(user_id=user_id, conn=conn):
            return cls.NOT_ADMIN

        cls.delete_process(conn=conn, user_id=user_id)
        return cls.SUCCESS_DEL

    @staticmethod
    def delete_process(user_id: int, conn: sq.Connection):
        cur = conn.cursor()

        cur.execute("""UPDATE users SET admin = 0 WHERE user_id LIKE(?)""", (user_id,))
        conn.commit()

    @staticmethod
    def is_user(user_id: int, conn: sq.Connection) -> bool:
        cur = conn.cursor()

        res = cur.execute("""SELECT activ FROM users WHERE user_id LIKE(?)""", (user_id,))
        if res.fetchone():
            return True
        else:
            return False

    @staticmethod
    def is_admin(user_id: int, conn: sq.Connection) -> bool:
        cur = conn.cursor()

        res = cur.execute("""SELECT admin FROM users WHERE user_id LIKE(?)""", (user_id,)).fetchone()

        if res and res[0] == 1:
            return True
        else:
            return False

    @staticmethod
    def get_users(conn: sq.Connection, regim: str = "all") -> list:
        cur = conn.cursor()

        if regim == "activ":
            ids_list = cur.execute("""SELECT user_id FROM users WHERE activ == 1""").fetchall()
        else:
            ids_list = cur.execute("""SELECT user_id FROM users""").fetchall()

        return ids_list

    @staticmethod
    def update_activ_date(user_id: int, date: str, conn: sq.Connection) -> None:
        cur = conn.cursor()

        cur.execute("UPDATE users SET activ = 1, last_active_date = ? WHERE user_id = ?", (date, user_id))
        conn.commit()

    @staticmethod
    def update_activ_status(user_id: int, conn: sq.Connection) -> None:
        cur = conn.cursor()

        cur.execute("""UPDATE users SET activ = 0 WHERE user_id LIKE(?)""", (user_id, ))
        conn.commit()
