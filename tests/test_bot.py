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
    assert_message_sent(bot_mock, chat_member_mock.chat.id,
                        'Привет @Joss!\nВыберите язык с которого нужно перевести',
                        [
                            ["украинский", 'l|123|ua||'],
                            ["русский", 'l|123|ru||'],
                        ])


def create_mock_user() -> types.User:
    return Mock(id=ID, username=NAME, full_name=NAME)


def assert_message_sent(bot_mock: AsyncMock, chat_id: AsyncMock,
                        expected_message: str, buttons: list[list[str]]):
    bot_mock.send_message.assert_called_once()
    assert 2 == len(bot_mock.send_message.call_args.args)
    assert chat_id == bot_mock.send_message.call_args.args[0]
    assert expected_message == bot_mock.send_message.call_args.args[1]
    assert 1 == len(bot_mock.send_message.call_args.kwargs)
    markup = bot_mock.send_message.call_args.kwargs["reply_markup"]
    assert isinstance(markup, types.InlineKeyboardMarkup)
    assert len(buttons) == len(markup.inline_keyboard)
    for button_index, expected_button in enumerate(buttons):
        assert 1 == len(markup.inline_keyboard[button_index])
        button = markup.inline_keyboard[button_index][0]
        assert expected_button[0] == button.text
        assert expected_button[1] == button.callback_data
