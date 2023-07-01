from datetime import datetime
import sqlite3

TABLE = "translator_options"
TABLE_DEF = f"CREATE TABLE IF NOT EXISTS {TABLE}" + \
    "(user_id INTEGER PRIMARY KEY, date_sent INTEGER)"


class Storage:
    _con: sqlite3.Connection

    def __init__(self, db: str):
        self._con = sqlite3.connect(db)
        self._con.execute(TABLE_DEF)
        self._con.commit()

    def record_translator_option(self, user_id: int):
        self._con.execute(
            f"REPLACE INTO {TABLE} (user_id, date_sent) values (?, STRFTIME('%s'))",
            [user_id])
        self._con.commit()

    def last_translator_option_time(self, user_id: int) -> datetime | None:
        cur = self._con.cursor()
        cur.execute(f"SELECT date_sent FROM {TABLE} WHERE user_id = ?", [user_id])
        row = cur.fetchone()
        if row is None:
            return None
        return datetime.fromtimestamp(row[0])
