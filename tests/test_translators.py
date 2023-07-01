from bot.translators import TranslatorsData


def make_test_data():
    return TranslatorsData([{
        "id": "1",
        "createdTime": "2022-05-01T21:39:26.000Z",
        "fields": {
              "Имя": "test1",
              "Языки": ["английский", "русский"],
              "Телеграм-аккаунт": "@test"
        }
    }, {
        "id": "2",
        "createdTime": "2022-05-01T21:39:26.000Z",
        "fields": {
              "Имя": "test1",
              "Языки": ["английский", "испанский", "русский"],
              "Телеграм-аккаунт": "@test2"
        }
    }, {
        "id": "3",
        "createdTime": "2022-05-01T21:39:26.000Z",
        "fields": {
              "Имя": "test2",
        }
    }])


def test_get_language_pairs():
    data = make_test_data()
    assert ["английский", "испанский"] == data.available_targets("русский")


def test_find_next_translator():
    data = make_test_data()
    assert None is data.find_next_translator("русский", "немецкий", 0)
    assert "@test" == data.find_next_translator("русский", "английский", 0)
    assert "@test2" == data.find_next_translator(
        "русский", "английский", 0, "@test")
    assert "@test" == data.find_next_translator(
        "русский", "английский", 0, "bad name")
