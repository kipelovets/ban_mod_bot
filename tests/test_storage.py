from datetime import datetime
from bot.storage import Storage

def test_record_translator_option():
    sut = Storage("test.sqlite")
    sut.record_translator_option(123)
    result = sut.last_translator_option_time(123)
    assert result is not None
    assert datetime.now().timestamp() - result.timestamp() < 1.0
