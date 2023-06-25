from datetime import datetime
import sqlite3

TABLE = "translator_options"
TABLE_DEF = f"CREATE TABLE IF NOT EXISTS {TABLE}" + \
    "(user_id INTEGER PRIMARY KEY, date_sent INTEGER)"


class Storage:
    con: sqlite3.Connection

    def __init__(self, db: str):
        self.con = sqlite3.connect(db)
        self.con.execute(TABLE_DEF)
        self.con.commit()

    def record_translator_option(self, user_id: int):
        self.con.execute(
            f"INSERT INTO {TABLE} (user_id, date_sent) values (?, unixepoch())",
            [user_id])
        self.con.commit()

    def last_translator_option_time(self, user_id: int) -> datetime | None:
        cur = self.con.cursor()
        cur.execute(f"SELECT date_sent FROM {TABLE} WHERE user_id = ?", [user_id])
        row = cur.fetchone()
        if row is None:
            return None
        return datetime.fromtimestamp(row[0])
