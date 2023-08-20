import sqlite3 as sq
from configs.config import db_name


def update_activ_date(user_id: int, date: str) -> None:
    with sq.connect(db_name) as con:
        cur = con.cursor()
        cur.execute("UPDATE users SET activ = 1, last_active_date = ? WHERE user_id = ?", (date, user_id))
