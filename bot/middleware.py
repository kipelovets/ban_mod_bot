import dataclasses
import logging
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.analytics import Analytics

from bot.data import LingvoData
from bot.handlers.gc import GC

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class LingvoDataMiddleware(BaseMiddleware):
    def __init__(self, lingvo_data: LingvoData, analytics: Analytics, gc: GC):
        self.lingvo_data = lingvo_data
        self.analytics = analytics
        self.gc = gc
        BaseMiddleware.__init__(self)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data["lingvo_data"] = self.lingvo_data
        data["analytics"] = self.analytics
        data["gc"] = self.gc
        result = await handler(event, data)
        return result
