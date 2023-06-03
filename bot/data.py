from bot.messages.messages import Messages
from .storage import TranslatorsData


class LingvoData:
    def __init__(self, data: TranslatorsData, messages: Messages):
        self.data = data
        self.messages = messages
