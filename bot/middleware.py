import dataclasses
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.analytics import Analytics

from bot.data import LingvoData

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class LingvoDataMiddleware(BaseMiddleware):
    def __init__(self, lingvo_data: LingvoData, analytics: Analytics):
        self.lingvo_data = lingvo_data
        self.analytics = analytics
        BaseMiddleware.__init__(self)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["lingvo_data"] = self.lingvo_data
        data["analytics"] = self.analytics
        result = await handler(event, data)
        return result
