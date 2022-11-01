class Messages:
    translations: dict

    def __init__(self, translations: dict):
        self.translations = translations

    def can_not_reply_to_foreign_message(self) -> str:
        return self.translations['can_not_reply_to_foreign_message']

    def welcome_choose_initial_language(self, username: str) -> str:
        return self.translations['welcome_choose_initial_language'].format(username=username)

    def choose_target_language(self, username: str, from_lang: str) -> str:
        return self.translations['choose_target_language'].format(
            username=username, from_lang=from_lang)

    def no_translators_found(self, username: str, from_lang: str, to_lang: str) -> str:
        return self.translations['no_translators_found'].format(
            username=username, from_lang=from_lang, to_lang=to_lang)

    def next_translator(self, username: str, from_lang: str, to_lang: str, translator: str) -> str:
        return self.translations['next_translator'].format(
            username=username, from_lang=from_lang, to_lang=to_lang, translator=translator)

    def button_back(self) -> str:
        return self.translations['button_back']

    def button_next_translator(self) -> str:
        return self.translations['button_next_translator']
