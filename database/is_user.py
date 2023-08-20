import sqlite3 as sq
from configs.config import db_name


def is_user(user_id: int) -> bool:
    with sq.connect(db_name) as con:
        cur = con.cursor()

        res = cur.execute("""SELECT activ FROM users WHERE user_id LIKE(?)""", (user_id, ))
        if res.fetchone():
            return True
        else:
            return False
