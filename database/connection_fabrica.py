import sqlite3 as sq


def get_connection(my_db_name: str) -> sq.Connection:
    my_connection = sq.connect(my_db_name)
    return my_connection
