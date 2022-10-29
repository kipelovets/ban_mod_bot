from unittest.mock import AsyncMock, Mock

from aiogram import types

from bot.handlers import echo, start
from bot.handlers.handlers import welcome

TEXT = "test123"
ID = 123
NAME = "Joss"


async def test_echo_handler():
    message_mock = AsyncMock(text=TEXT)
    await echo(message=message_mock)
    message_mock.answer.assert_called_once_with(TEXT)


async def test_handler_start():
    user_mock = create_mock_user()
    message_mock = AsyncMock(from_user=user_mock)
    await start(message=message_mock)


async def test_handler_welcome():
    user_mock = create_mock_user()
    new_chat_member_mock = Mock(user=user_mock)
    bot_mock = AsyncMock()
    chat_mock = Mock(id=ID)
    chat_member_mock = Mock(
        new_chat_member=new_chat_member_mock, bot=bot_mock, chat=chat_mock)
    await welcome(chat_member=chat_member_mock)
    bot_mock.send_message.assert_called_once()
    assert 2 == len(bot_mock.send_message.call_args.args)
    assert chat_member_mock.chat.id == bot_mock.send_message.call_args.args[0]
    assert 'Привет @Joss!\nВыберите язык с которого нужно перевести' == bot_mock.send_message.call_args.args[1]
    assert 1 == len(bot_mock.send_message.call_args.kwargs)
    markup = bot_mock.send_message.call_args.kwargs["reply_markup"]
    assert isinstance(markup, types.InlineKeyboardMarkup)
    assert 2 == len(markup.inline_keyboard)
    assert 1 == len(markup.inline_keyboard[0])
    button = markup.inline_keyboard[0][0]
    assert "украинский" == button.text
    assert 'l|123|ua||' == button.callback_data


def create_mock_user() -> types.User:
    return Mock(id=ID, username=NAME, full_name=NAME)
