import pytest
from bot.language import code_by_lang, lang_by_code


def test_lang_by_code():
    assert "украинский" == lang_by_code("ua")
    with pytest.raises(ValueError):
        _ = lang_by_code("BAD CODE")


def test_code_by_lang():
    assert "ru" == code_by_lang("русский")
    with pytest.raises(ValueError):
        _ = code_by_lang("BAD LANGUAGE")
