from ga4mp import GtagMP


class Analytics:
    def __init__(self, api_secret: str, measurement_id: str, client_id: str):
        self.ga = GtagMP(measurement_id=measurement_id,
                         api_secret=api_secret,
                         client_id=client_id)

    def bot_started(self):
        self._event("started", env="local")

    def language_pair_selected(self, lang_from: str, lang_to: str):
        self._event("language_pair_selected", lang_from=lang_from, lang_to=lang_to)

    def chat_member(self, user_id: int):
        self._event("chat_member", user_id=str(user_id))

    def start(self, user_id: int):
        self._event("start", user_id=str(user_id))

    def finish(self, user_id: int):
        self._event("finish", user_id=str(user_id))

    def select_from_language(self, user_id: int):
        self._event("select_from_language", user_id=str(user_id))

    def select_to_language(self, user_id: int, lang_from: str):
        self._event("select_to_language", user_id=str(user_id), lang_from=lang_from)

    def translator_option(self, user_id: int, lang_from: str, lang_to: str, translator: str):
        self._event("translator_option", user_id=str(user_id), lang_from=lang_from,
                    lang_to=lang_to, translator=translator)

    def no_translator_option(self, user_id: int, lang_from: str, lang_to: str):
        self._event("translator_option", user_id=str(user_id), lang_from=lang_from,
                    lang_to=lang_to)

    def _event(self, name: str, **kwargs: str):
        event = self.ga.create_new_event(name=name)
        for key, value in kwargs.items():
            event.set_event_param(name=key, value=value)
        self.ga.send(events=[event])
