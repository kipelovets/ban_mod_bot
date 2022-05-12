from pyairtable import Table

def load(api_key: str, base_id: str, table_name: str):
  table = Table(api_key, base_id, table_name)
  return table.all()