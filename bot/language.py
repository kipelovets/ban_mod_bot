RU = 'русский'
UA = 'украинский'

languages = {
    'ka': 'грузинский',
    'sv': 'шведский',
    'he': 'иврит',
    'ar': 'арабский',
    'ca': 'каталанский',
    'pl': 'польский',
    'af': 'африкаанс',
    'no': 'норвежский',
    'sl': 'словенский',
    'fr': 'французский',
    'de': 'немецкий',
    'mn': 'монгольский',
    'hr': 'хорватский',
    'da': 'датский',
    'be': 'белорусский',
    'lv': 'латышский',
    'en': 'английский',
    'fi': 'финский',
    'bg': 'болгарский',
    'hi': 'хинди',
    'ru': 'русский',
    'cs': 'чешский',
    'pt': 'португальский',
    'lt': 'литовский',
    'th': 'тайский',
    'el': 'греческий',
    'sr': 'сербский',
    'ro': 'румынский',
    'jp': 'японский',
    'zh': 'китайский',
    'ua': 'украинский',
    'sk': 'словацкий',
    'hg': 'венгерский',
    'ko': 'корейский',
    'nl': 'нидерландский',
    'et': 'эстонский',
    'tr': 'турецкий',
    'es': 'испанский',
    'uz': 'узбекский',
    'it': 'итальянский'}


def lang_by_code(code: str) -> str:
    if code not in languages:
        raise ValueError(f"Language '{code}' is not found")
    return languages[code]


def code_by_lang(lang: str | None) -> str:
    values = list(languages.values())
    if lang is None or lang not in values:
        raise ValueError(f"Language '{lang}' is not found")
    return list(languages.keys())[values.index(lang)]
