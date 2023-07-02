import logging
from pyairtable.api.table import Table
from ..language import RU

logger = logging.getLogger(__name__)


class Messages:
    translations: dict[str, dict[str, str]]

    def __init__(self, translations: dict[str, dict[str, str]]):
        self.translations = {}
        for key, trs in translations.items():
            self.translations[key] = {}
            for lang, val in trs.items():
                self.translations[key][lang] = val.replace("\\n", "\n")

    def can_not_reply_to_foreign_message(self) -> str:
        return self._t('can_not_reply_to_foreign_message', RU)

    def choose_from_language(self, username: str) -> str:
        return self._t('choose_from_language', RU).format(username=username)

    def welcome_choose_popular_pairs(self, username: str) -> str:
        return self._t('welcome_choose_popular_pairs', RU).format(username=username)

    def choose_target_language(self, username: str, from_lang: str) -> str:
        return self._t('choose_target_language', from_lang).format(
            username=username, from_lang=from_lang)

    def no_translators_found(self, username: str, from_lang: str, to_lang: str) -> str:
        return self._t('no_translators_found', from_lang).format(
            username=username, from_lang=from_lang, to_lang=to_lang)

    def next_translator(self, username: str, from_lang: str, to_lang: str, translator: str) -> str:
        return self._t('next_translator', from_lang).format(
            username=username, from_lang=from_lang, to_lang=to_lang, translator=translator)

    def button_back(self, from_lang: str) -> str:
        return self._t('button_back', from_lang)

    def button_next_translator(self, from_lang: str) -> str:
        return self._t('button_next_translator', from_lang)

    def button_finish(self, from_lang: str) -> str:
        return self._t("button_finish", from_lang)

    def finished(self, from_lang: str) -> str:
        return self._t("finished", from_lang)

    def message_expired(self) -> str:
        return self._t("message_expired", RU)

    def next_translator_timeout(self, from_lang: str) -> str:
        return self._t("next_translator_timeout", from_lang)

    def other_languages(self, from_lang: str) -> str:
        return self._t("other_languages", from_lang)

    def no_help_needed(self, from_lang: str) -> str:
        return self._t("no_help_needed", from_lang)

    def welcome_to_chat(self, username: str, from_lang: str) -> str:
        return self._t("welcome_to_chat", from_lang).format(username=username)

    def find_text_translator(self, from_lang: str) -> str:
        return self._t("find_text_translator", from_lang)

    def find_voice_translator(self, from_lang: str) -> str:
        return self._t("find_voice_translator", from_lang)

    def restart(self, from_lang: str) -> str:
        return self._t("restart", from_lang)

    def _t(self, key: str, from_lang: str) -> str:
        if key not in self.translations or from_lang not in self.translations[key]:
            raise KeyError(f"Translation not found: '{key}', '{from_lang}'")
        return self.translations[key][from_lang]


def load_messages(api_key: str, base_id: str, table_name: str) -> Messages:
    table = Table(api_key, base_id, table_name)

    data = {}
    rec: dict[str, dict[str, str]]
    for rec in table.all():
        data[rec['fields']['id']] = rec['fields']

    logger.info("loaded messages: %s", len(data))

    return Messages(data)
