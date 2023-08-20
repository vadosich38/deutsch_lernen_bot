import sqlite3 as sq


def create_db(name: str) -> None:
    with sq.connect(name) as con:
        cur = con.cursor()

        # cur.execute("""DROP TABLE IF EXISTS users""")

        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER,
                        admin INTEGER,
                        activ INTEGER,
                        last_active_date TEXT)""")
