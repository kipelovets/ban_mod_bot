
from aiogram import types

async def echo(message: types.Message):
    await message.answer(message.text)

async def start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Украинский", callback_data="from:ua"))
    keyboard.add(types.InlineKeyboardButton(text="Русский", callback_data="from:ru"))
    await message.answer("Выберите язык с которого нужно перевести", reply_markup=keyboard)

async def select_language(call: types.CallbackQuery):
    langType, lang = call.data.split(":") 
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Украинский", callback_data="to:ua"))
    keyboard.add(types.InlineKeyboardButton(text="Русский", callback_data="to:ru"))
    await call.message.edit_text(f"Язык документа: {lang}\nТеперь выберите язык на который нужно перевести: ", reply_markup=keyboard)
    await call.answer("Спасибо!")