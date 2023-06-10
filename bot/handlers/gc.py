import asyncio
import logging
from dataclasses import dataclass
from aiogram import Bot

logger = logging.getLogger(__name__)
MESSAGE = "This message expired\nPlease contact the bot directly: @lingvo_catalogue_bot"


@dataclass
class Task:
    chat_id: int
    message_id: int
    time: int


class GC:
    time: int = 0
    queue: list[Task] = []
    bot: Bot

    def __init__(self, bot: Bot):
        self.bot = bot
        asyncio.get_running_loop().create_task(self.check_queue())

    async def check_queue(self):
        while True:
            await asyncio.sleep(1)
            self.time += 1
            ready = [x for x in self.queue if x.time <= self.time]
            if len(ready) == 0:
                continue
            for task in ready:
                try:
                    self.queue.remove(task)
                    await self.bot.edit_message_text(MESSAGE, task.chat_id, task.message_id)
                except Exception as e:
                    logger.error(type(e))

    async def add_to_queue(self, chat_id: int, message_id: int, after: int):
        self.queue[:] = [x for x in self.queue
                         if x.chat_id != chat_id or x.message_id != message_id]
        self.queue.append(Task(chat_id, message_id, self.time + after))
