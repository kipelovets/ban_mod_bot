import os
import sys
from bot.data import LingvoData
from bot.messages import load_messages
from bot.storage import load


def load_lingvo_data() -> LingvoData:
    api_key = os.getenv('AIRTABLE_API_KEY')
    base_id = os.getenv('AIRTABLE_BASE_ID')
    table_name = os.getenv('AIRTABLE_TABLE_NAME')
    messages_table_name = os.getenv('AIRTABLE_MESSAGES_TABLE_NAME')
    if api_key is None or base_id is None or table_name is None or \
            messages_table_name is None:
        print("Error: required env vars not defined")
        sys.exit(1)

    return LingvoData(
        load(api_key, base_id, table_name),
        load_messages(api_key, base_id, messages_table_name))
