
from aiogram import types

async def echo(message: types.Message):
    await message.answer(message.text)

async def start(message: types.Message):
    await message.answer("Hello, I'm a bot v3")
