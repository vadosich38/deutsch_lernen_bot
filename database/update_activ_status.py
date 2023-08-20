import sqlite3 as sq
from configs.config import db_name


def update_activ_status(user_id: int) -> None:
    with sq.connect(db_name) as con:
        cur = con.cursor()

        cur.execute("""UPDATE users SET activ = 0 WHERE user_id LIKE(?)""", (user_id, ))
