from bot.language import code_by_lang, lang_by_code


def test_lang_by_code():
    assert "украинский" == lang_by_code("ua")
    assert None == lang_by_code("BAD CODE")


def test_code_by_lang():
    assert "ru" == code_by_lang("русский")
    assert None == code_by_lang("BAD LANGUAGE")
