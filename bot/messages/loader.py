from pyairtable.api.table import Table

from .messages import Messages


def load_messages(api_key: str, base_id: str, table_name: str) -> Messages:
    table = Table(api_key, base_id, table_name)

    data = {}
    rec: dict[str, dict[str, str]]
    for rec in table.all():
        data[rec['fields']['id']] = rec['fields']

    return Messages(data)
