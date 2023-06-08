# pyright: reportUnknownVariableType=false

from unittest.mock import AsyncMock, Mock

from aiogram import types

from bot.messages import Messages
from bot.language import RU, UA

TEXT = "test123"
ID = 123
NAME = "Joss"

NEXT_TRANSLATOR_MSG = "Привет @{username}!\n" + \
    "Следующий переводчик для пары {from_lang} - {to_lang}: {translator}"


def given_messages() -> Messages:
    return Messages({
        "can_not_reply_to_foreign_message": {RU: "Вы не можете отвечать на чужое сообщение!"},
        "choose_from_language": {RU: "Привет @{username}!\nВыберите:"},
        "choose_target_language": {
            RU: "Привет @{username}!\nВыбранный язык: {from_lang}\nТеперь:",
            UA: "[UA] Привет @{username}!\nВыбранный язык: {from_lang}\nТеперь:"
        },
        "button_back": {UA: "Назад"},
        "button_next_translator": {UA: "Следующий переводчик"},
        "next_translator": {UA: NEXT_TRANSLATOR_MSG},
        "button_finish": {UA: "_ button finish"},
        "welcome_choose_popular_pairs": {RU: "_ welcome {username}"}
    })


def given_new_chat_member() -> Mock:
    user_mock = given_user()
    new_chat_member_mock = Mock(user=user_mock, status="member")
    bot_mock = AsyncMock()
    chat_mock = Mock(id=ID)
    return Mock(
        new_chat_member=new_chat_member_mock, bot=bot_mock, chat=chat_mock)


def given_user() -> types.User:
    return Mock(id=ID, username=NAME, full_name=NAME)


def given_callback_query() -> Mock:
    return AsyncMock(from_user=given_user())


def then_answer(message_mock: AsyncMock, expected_message: str,
                expected_buttons: list[list[types.InlineKeyboardButton]]) -> None:
    message_mock.answer.assert_called_once()
    assert 1 == len(message_mock.answer.call_args.args)
    assert expected_message == message_mock.answer.call_args.args[0], \
        f"Wrong message: {message_mock.answer.call_args.args[0]}"
    assert 1 == len(message_mock.answer.call_args.kwargs)
    markup: Mock = message_mock.answer.call_args.kwargs["reply_markup"]
    then_inline_keyboard(markup, expected_buttons)


def then_message_edited(message: AsyncMock, expected_message: str,
                        expected_buttons: list[list[types.InlineKeyboardButton]]) -> None:
    message.edit_text.assert_called_once()
    assert 1 == len(message.edit_text.call_args.args)
    assert expected_message == message.edit_text.call_args.args[
        0], f"Wrong message: {message.edit_text.call_args.args[0]}"
    assert 1 == len(message.edit_text.call_args.kwargs)
    markup: Mock = message.edit_text.call_args.kwargs["reply_markup"]
    then_inline_keyboard(markup, expected_buttons)


def then_inline_keyboard(markup: Mock,
                         expected_buttons: list[list[types.InlineKeyboardButton]]) -> None:
    assert isinstance(markup, types.InlineKeyboardMarkup)
    assert len(expected_buttons) == len(markup.inline_keyboard), \
        f"Button rows: {len(markup.inline_keyboard)} != {len(expected_buttons)}"
    for row_index, expected_button_row in enumerate(expected_buttons):
        assert len(expected_button_row) == len(
            markup.inline_keyboard[row_index])
        for col_index, expected_button in enumerate(expected_button_row):
            button: types.InlineKeyboardButton = markup.inline_keyboard[row_index][col_index]
            assert expected_button.text == button.text, \
                f"Button {expected_button.text} != {button.text}"
            assert expected_button.callback_data == button.callback_data, \
                f"Data {expected_button.callback_data} != {button.callback_data}"


def then_message_sent(bot_mock: AsyncMock, chat_id: AsyncMock, expected_message: str,
                      expected_buttons: list[list[types.InlineKeyboardButton]]) -> None:
    bot_mock.send_message.assert_called_once()
    assert 2 == len(bot_mock.send_message.call_args.args)
    assert chat_id == bot_mock.send_message.call_args.args[0]
    assert expected_message == bot_mock.send_message.call_args.args[1],\
        f"Message {expected_message} != {bot_mock.send_message.call_args.args[1]}"
    assert 1 == len(bot_mock.send_message.call_args.kwargs)
    markup: Mock = bot_mock.send_message.call_args.kwargs["reply_markup"]
    then_inline_keyboard(markup, expected_buttons)
