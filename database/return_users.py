import sqlite3 as sq
from configs.config import db_name


def get_users(regim: str = "all") -> list:
    with sq.connect(db_name) as con:
        cur = con.cursor()

        if regim == "all":
            ids_list = cur.execute("""SELECT user_id FROM users""").fetchall()
            return ids_list
        if regim == "activ":
            ids_list = cur.execute("""SELECT user_id FROM users WHERE activ == 1""").fetchall()
            return ids_list
