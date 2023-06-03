from unittest.mock import AsyncMock, Mock

from aiogram import types

import bot.handlers.handlers as handler
from bot.data import LingvoData
from bot.handlers.utils import make_cb
from .utils import given_messages, given_user, \
    given_new_chat_member, given_callback_query, ID, \
    then_message_edited, then_message_sent, then_answer

WELCOME_KEYBOARD = [
    [types.InlineKeyboardButton(
        text="украинский", callback_data='l|123|ua||')],
    [types.InlineKeyboardButton(
        text="русский", callback_data='l|123|ru||')],
]

mock_data = Mock()
mock_data.get_language_pairs = Mock(
    return_value={"немецкий", "английский", "грузинский"})
mock_data.find_next_translator = Mock(return_value="translator_username")
mock_data.find_all_languages = Mock(
    return_value={"русский", "украинский", "немецкий", "английский", "грузинский"})

mock_lingvo_data = LingvoData(mock_data, given_messages())


async def test_start():
    user_mock = given_user()
    message_mock = AsyncMock(from_user=user_mock)
    await handler.start(message_mock, mock_lingvo_data)
    then_answer(
        message_mock, "Привет @Joss!\nВыберите:", WELCOME_KEYBOARD)


async def test_welcome():
    chat_member_mock = given_new_chat_member()
    await handler.welcome(chat_member_mock,
                          mock_lingvo_data,
                          chat_member_mock.bot)
    then_message_sent(chat_member_mock.bot, chat_member_mock.chat.id,
                      'Привет @Joss!\nВыберите:',
                      WELCOME_KEYBOARD)


async def test_select_from_language():
    call = given_callback_query()
    await handler.select_from_language(call, make_cb(ID), mock_lingvo_data)
    call.answer.assert_not_called()
    then_message_edited(call.message,
                        "Привет @Joss!\nВыберите:",
                        WELCOME_KEYBOARD)


async def test_select_from_language_clicked_by_another_user():
    call = given_callback_query()
    await handler.select_from_language(call, make_cb(ID + 1), mock_lingvo_data)
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()


async def test_select_language():
    call = given_callback_query()
    await handler.select_language(call, make_cb(ID, "украинский"),
                                  mock_lingvo_data)
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
    await handler.select_language(call, make_cb(ID + 1, "украинский"),
                                  mock_lingvo_data)
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()


async def test_select_translator():
    call = given_callback_query()
    await handler.select_translator(call, make_cb(ID, "украинский", "немецкий"),
                                    mock_lingvo_data)

    expected_buttons = [
        [
            types.InlineKeyboardButton(
                text="Следующий переводчик", callback_data="l|123|ua|de|translator_username"), ], [
            types.InlineKeyboardButton(
                text="Назад", callback_data="l|123|ua||")]]
    then_message_edited(call.message,
                        """Привет @Joss!
Следующий переводчик для пары украинский - немецкий: translator_username""",
                        expected_buttons=expected_buttons)
    call.answer.assert_not_called()


async def test_select_translator_clicked_by_another_user():
    call = given_callback_query()
    await handler.select_translator(call, make_cb(ID + 1, "украинский", "немецкий"),
                                    mock_lingvo_data)
    call.answer.assert_called_once_with(
        "Вы не можете отвечать на чужое сообщение!")
    call.message.edit_text.assert_not_called()
