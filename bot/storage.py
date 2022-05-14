from pyairtable import Table


class TranslatorsData:
    def __init__(self, data: list[dict]):
        self.data = list(filter(
            lambda rec: "Языки" in rec["fields"] and "Телеграм-аккаунт" in rec["fields"], data))

    def get_language_pairs(self, lang: str) -> set[str]:
        result = set()
        for rec in self.data:
            langs = rec["fields"]["Языки"]
            if not lang in langs:
                continue
            for l in langs:
                if l != lang:
                    result.add(l)
        return result

    def find_next_translator(self, lang_from: str, lang_to: str, prev: str = None) -> str:
        if prev == "":
            prev = None
        found_prev = False
        for rec in self.data:
            langs = rec["fields"]["Языки"]
            if not lang_from in langs or not lang_to in langs:
                continue
            if prev != None and rec["fields"]["Телеграм-аккаунт"] == prev:
                found_prev = True
                continue
            if prev != None and not found_prev:
                continue
            return rec["fields"]["Телеграм-аккаунт"]
        return None

    def find_all_languages(self) -> set[str]:
        result = set()
        for rec in self.data:
            langs = rec["fields"]["Языки"]
            result.update(langs)
        return result


def load(api_key: str, base_id: str, table_name: str) -> TranslatorsData:
    table = Table(api_key, base_id, table_name)
    return TranslatorsData(table.all())
