import dataclasses
from bot.messages.messages import Messages
from .storage import TranslatorsData


@dataclasses.dataclass
class LingvoData:
    def __init__(self, data: TranslatorsData, messages: Messages):
        self.data = data
        self.messages = messages
