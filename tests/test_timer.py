from unittest.mock import Mock
from bot.timer import Timer


def test_timer():
    storage = Mock()
    storage.last_translator_option_time = Mock(return_value=None)
    sut = Timer(storage)
    result = sut.can_send_translator_option(123)
    assert result
