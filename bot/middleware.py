import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.data import LingvoData

logger = logging.getLogger(__name__)


class LingvoDataMiddleware(BaseMiddleware):
    def __init__(self, lingvo_data: LingvoData):
        print("!!!!")
        logger.critical("!!!!")
        self.lingvo_data = lingvo_data
        BaseMiddleware.__init__(self)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        print("Before handler")
        data["lingvo_data"] = self.lingvo_data
        result = await handler(event, data)
        print("After handler")
        return result
