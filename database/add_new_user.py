import sqlite3 as sq
from configs.config import db_name
from .is_user import is_user


def new_user_create(user_id: int, date: str) -> None:
    if not is_user(user_id=user_id):
        with sq.connect(db_name) as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO users VALUES(?, ?, ?, ?)""", (user_id, 0, 1, date, ))
