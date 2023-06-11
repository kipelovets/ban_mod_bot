import logging
import random
from typing import Any
from pyairtable.api.table import Table

logger = logging.getLogger(__name__)


class TranslatorsData:
    def __init__(self, data: list[dict[str, Any]]):
        self.data = list(filter(
            lambda rec: "Языки" in rec["fields"] and "Телеграм-аккаунт" in rec["fields"], data))

    def available_targets(self, lang: str) -> list[str]:
        result: set[str] = set()
        for rec in self.data:
            langs = rec["fields"]["Языки"]
            if lang not in langs:
                continue
            for other_lang in langs:
                if other_lang != lang:
                    result.add(other_lang)
        return sorted(result)

    def _find_translators(self, lang_from: str, lang_to: str) -> list[str]:
        result: list[str] = []
        for rec in self.data:
            langs = rec["fields"]["Языки"]
            if lang_from not in langs or lang_to not in langs:
                continue
            result.append(rec["fields"]["Телеграм-аккаунт"])
        return result

    def find_next_translator(self, lang_from: str, lang_to: str,
                             seed: int, prev: str | None = None) -> str | None:
        translators = self._find_translators(lang_from, lang_to)
        random.Random(seed).shuffle(translators)
        ind = 0
        if prev is not None:
            try:
                prev_index = translators.index(prev)
                ind = prev_index + 1
            except ValueError:
                pass
        if ind >= len(translators):
            return None
        return translators[ind]

    def find_all_languages(self) -> set[str]:
        result: set[str] = set()
        for rec in self.data:
            langs = rec["fields"]["Языки"]
            result.update(langs)
        return result


def load_translators(api_key: str, base_id: str, table_name: str) -> TranslatorsData:
    logger.info("Loading translators")
    table = Table(api_key, base_id, table_name)
    data: list[dict[str, Any]] = table.all()
    logger.info("loaded translators: %s", len(data))
    return TranslatorsData(data)
