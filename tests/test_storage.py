from bot.storage import TranslatorsData


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
    assert {"английский", "испанский"} == data.get_language_pairs("русский")


def find_next_translator():
    data = make_test_data()
    assert None is data.find_next_translator("русский", "немецкий")
    assert "@test" == data.find_next_translator("русский", "английский")
    assert "@test2" == data.find_next_translator(
        "русский", "английский", "@test")
    assert "@test2" == data.find_next_translator(
        "русский", "английский", "bad name")
