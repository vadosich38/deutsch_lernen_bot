import sqlite3 as sq
from configs.config import ADMIN, db_name


def is_admin(user_id: int) -> bool:
    with sq.connect(db_name) as con:
        cur = con.cursor()

        res = cur.execute("""SELECT admin FROM users WHERE user_id LIKE(?)""", (user_id, )).fetchone()

        if res and res[0] == 1:
            return True
        else:
            return False
