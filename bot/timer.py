# pylint: disable=too-few-public-methods
from datetime import datetime
from bot.storage import Storage

NEXT_TRANSLATOR_TIMEOUT = 60


class Timer:
    def __init__(self, storage: Storage):
        self._storage = storage

    def can_send_translator_option(self, user_id: int) -> bool:
        result = self._storage.last_translator_option_time(user_id)
        if result is not None and \
            datetime.now().timestamp() - result.timestamp() < NEXT_TRANSLATOR_TIMEOUT:
            return False
        self._storage.record_translator_option(user_id)
        return True
