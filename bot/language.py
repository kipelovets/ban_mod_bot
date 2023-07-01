RU = 'русский'
UA = 'украинский'
DE = 'немецкий'
EN = 'английский'
PL = 'польский'

OTHER_LANGUAGES = 'Другие языки'

popular_pairs = {
    "укр ↔ нем": (UA, DE),
    "рус ↔ нем": (RU, DE),
}

language_pretty = {
    DE: 'немецкий 🇩🇪',
    EN: 'английский 🇬🇧',
    PL: 'польский 🇵🇱',
}

languages = {
    'de': DE,
    'en': EN,
    'pl': PL,
    'ar': 'арабский',
    'af': 'африкаанс',
    'be': 'белорусский',
    'bg': 'болгарский',
    'hg': 'венгерский',
    'el': 'греческий',
    'ka': 'грузинский',
    'da': 'датский',
    'he': 'иврит',
    'es': 'испанский',
    'it': 'итальянский',
    'ca': 'каталанский',
    'zh': 'китайский',
    'ko': 'корейский',
    'lv': 'латышский',
    'lt': 'литовский',
    'mn': 'монгольский',
    'nl': 'нидерландский',
    'no': 'норвежский',
    'pt': 'португальский',
    'ro': 'румынский',
    'ru': 'русский',
    'sr': 'сербский',
    'sk': 'словацкий',
    'sl': 'словенский',
    'th': 'тайский',
    'tr': 'турецкий',
    'uz': 'узбекский',
    'ua': 'украинский',
    'fi': 'финский',
    'fr': 'французский',
    'hi': 'хинди',
    'hr': 'хорватский',
    'cs': 'чешский',
    'sv': 'шведский',
    'et': 'эстонский',
    'jp': 'японский',
}


def lang_by_code(code: str | None) -> str:
    if code is None or code not in languages:
        raise ValueError(f"Language '{code}' is not found")
    return languages[code]


def code_by_lang(lang: str | None) -> str:
    values = list(languages.values())
    if lang is None or lang not in values:
        raise ValueError(f"Language '{lang}' is not found")
    return list(languages.keys())[values.index(lang)]


def prettify_lang(lang: str | None) -> str:
    if lang is None:
        raise ValueError(f"Language '{lang}' not found")
    if lang in language_pretty:
        return language_pretty[lang]
    return lang
