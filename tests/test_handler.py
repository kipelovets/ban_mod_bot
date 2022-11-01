from unittest.mock import AsyncMock, Mock

from aiogram import types

from bot.handlers import Handler
from bot.messages import Messages

TEXT = "test123"
ID = 123
NAME = "Joss"


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
        message_mock, "Привет @Joss!\nВыберите язык с которого нужно перевести", [
            [types.InlineKeyboardButton(
                text="украинский", callback_data='l|123|ua||')],
            [types.InlineKeyboardButton(
                text="русский", callback_data='l|123|ru||')],
        ])


async def test_welcome():
    chat_member_mock = given_new_chat_member()
    handler = given_handler()
    await handler.welcome(chat_member=chat_member_mock)
    then_message_sent(chat_member_mock.bot, chat_member_mock.chat.id,
                      'Привет @Joss!\nВыберите язык с которого нужно перевести',
                      [
                          [types.InlineKeyboardButton(
                              text="украинский", callback_data='l|123|ua||')],
                          [types.InlineKeyboardButton(
                              text="русский", callback_data='l|123|ru||')],
                      ])


async def test_select_from_language():
    handler = given_handler()
    call = given_callback_query()
    callback_data = {"user_id": ID}
    await handler.select_from_language(call, callback_data)
    call.answer.assert_not_called()
    then_message_edited(call.message,
                        "Привет @Joss!\nВыберите язык с которого нужно перевести",
                        [
                            [types.InlineKeyboardButton(
                                text="украинский", callback_data='l|123|ua||')],
                            [types.InlineKeyboardButton(
                                text="русский", callback_data='l|123|ru||')],
                        ])


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
    expected_message = """Привет @Joss!
Выбранный язык документа: украинский
Теперь выберите язык на который нужно перевести:"""
    then_message_edited(
        call.message, expected_message, [
            [
                types.InlineKeyboardButton(
                    text="английский", callback_data='l|123|ua|en|'), types.InlineKeyboardButton(
                    text="немецкий", callback_data='l|123|ua|de|')], [
                        types.InlineKeyboardButton(
                            text="Назад", callback_data="l|123|||")], ])


def given_messages() -> Messages:
    return Messages({
        "can_not_reply_to_foreign_message": "Вы не можете отвечать на чужое сообщение!",
        "welcome_choose_initial_language": "Привет @{username}!\nВыберите язык с которого нужно перевести",
        "choose_target_language": "Привет @{username}!\nВыбранный язык документа: {from_lang}\nТеперь выберите язык на который нужно перевести:",
    })


def given_handler() -> Handler:
    data = Mock()
    data.get_language_pairs = Mock(
        return_value={"немецкий", "английский", "польский"})
    data.find_next_translator = Mock(return_value="translator_username")
    data.find_all_languages = Mock(
        return_value={"русский", "украинский", "немецкий"})
    return Handler(data, given_messages())


def given_new_chat_member() -> Mock:
    user_mock = given_user()
    new_chat_member_mock = Mock(user=user_mock)
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
    assert expected_message == message_mock.answer.call_args.args[0]
    assert 1 == len(message_mock.answer.call_args.kwargs)
    markup = message_mock.answer.call_args.kwargs["reply_markup"]
    then_inline_keyboard(markup, expected_buttons)


def then_message_edited(message: AsyncMock, expected_message: str,
                        expected_buttons: list[list[types.InlineKeyboardButton]]) -> None:
    message.edit_text.assert_called_once()
    assert 1 == len(message.edit_text.call_args.args)
    assert expected_message == message.edit_text.call_args.args[0]
    assert 1 == len(message.edit_text.call_args.kwargs)
    markup = message.edit_text.call_args.kwargs["reply_markup"]
    then_inline_keyboard(markup, expected_buttons)


def then_inline_keyboard(markup: Mock,
                         expected_buttons: list[list[types.InlineKeyboardButton]]) -> None:
    assert isinstance(markup, types.InlineKeyboardMarkup)
    assert len(expected_buttons) == len(markup.inline_keyboard)
    for row_index, expected_button_row in enumerate(expected_buttons):
        assert len(expected_button_row) == len(
            markup.inline_keyboard[row_index])
        for col_index, expected_button in enumerate(expected_button_row):
            button = markup.inline_keyboard[row_index][col_index]
            assert expected_button.text == button.text
            assert expected_button.callback_data == button.callback_data


def then_message_sent(bot_mock: AsyncMock, chat_id: AsyncMock, expected_message: str,
                      expected_buttons: list[list[types.InlineKeyboardButton]]) -> None:
    bot_mock.send_message.assert_called_once()
    assert 2 == len(bot_mock.send_message.call_args.args)
    assert chat_id == bot_mock.send_message.call_args.args[0]
    assert expected_message == bot_mock.send_message.call_args.args[1]
    assert 1 == len(bot_mock.send_message.call_args.kwargs)
    markup = bot_mock.send_message.call_args.kwargs["reply_markup"]
    then_inline_keyboard(markup, expected_buttons)
