from unittest.mock import AsyncMock

from aiogram import types

from .utils import TEXT, ID, given_handler, given_callback_query, given_new_chat_member, \
    given_user, then_answer, then_message_edited, then_message_sent

WELCOME_KEYBOARD = [
    [types.InlineKeyboardButton(
        text="украинский", callback_data='l|123|ua||')],
    [types.InlineKeyboardButton(
        text="русский", callback_data='l|123|ru||')],
]


async def test_echo():
    message_mock = AsyncMock(text=TEXT)
    handler = given_handler()
    await handler.echo(message=message_mock)
    message_mock.answer.assert_called_once_with(TEXT)


async def test_start():
    user_mock = given_user()
    message_mock = AsyncMock(from_user=user_mock)
    handler = given_handler()
    await handler.start(message=message_mock)
    then_answer(
        message_mock, "Привет @Joss!\nВыберите:", WELCOME_KEYBOARD)


async def test_welcome():
    chat_member_mock = given_new_chat_member()
    handler = given_handler()
    await handler.welcome(chat_member=chat_member_mock)
    then_message_sent(chat_member_mock.bot, chat_member_mock.chat.id,
                      'Привет @Joss!\nВыберите:',
                      WELCOME_KEYBOARD)


async def test_select_from_language():
    handler = given_handler()
    call = given_callback_query()
    callback_data: dict[str, int | str] = {"user_id": ID}
    await handler.select_from_language(call, callback_data)
    call.answer.assert_not_called()
    then_message_edited(call.message,
                        "Привет @Joss!\nВыберите:",
                        WELCOME_KEYBOARD)


async def test_select_from_language_clicked_by_another_user():
    call = given_callback_query()
    await given_handler().select_from_language(call, {"user_id": ID + 1})
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()


async def test_select_language():
    call = given_callback_query()
    await given_handler().select_language(call, {"user_id": ID, "from_lang": "ua"})
    call.answer.assert_not_called()
    expected_message = """[UA] Привет @Joss!
Выбранный язык: украинский
Теперь:"""
    then_message_edited(
        call.message, expected_message, [
            [
                types.InlineKeyboardButton(text="английский", callback_data='l|123|ua|en|'),
                types.InlineKeyboardButton(text="грузинский", callback_data='l|123|ua|ka|')
            ],
            [
                types.InlineKeyboardButton(text="немецкий", callback_data='l|123|ua|de|'),
            ],
            [
                types.InlineKeyboardButton(text="Назад", callback_data="l|123|||")
            ],
        ])


async def test_select_language_clicked_by_another_user():
    call = given_callback_query()
    await given_handler().select_language(call, {"user_id": ID + 1, "from_lang": "ua"})
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()


async def test_select_translator():
    call = given_callback_query()
    await given_handler().select_translator(call, {"user_id": str(ID), "from_lang": "ua",
                                                   "to_lang": "de", "prev_translator": ""})
    then_message_edited(call.message,
                        """Привет @Joss!
Следующий переводчик для пары украинский - немецкий: translator_username""",
                        [[types.InlineKeyboardButton(text="Следующий переводчик",
                                                     callback_data="l|123|ua|de|translator_username"),
                          ],
                         [types.InlineKeyboardButton(text="Назад",
                                                     callback_data="l|123|ua||")]])
    call.answer.assert_not_called()


async def test_select_translator_clicked_by_another_user():
    call = given_callback_query()
    await given_handler().select_translator(call, {"user_id": str(ID + 1), "from_lang": "ua",
                                                   "to_lang": "de", "prev_translator": ""})
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()
