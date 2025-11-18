from azure.data.tables import TableServiceClient
import pandas as pd
def get_table_storage_df(conn_dict):
    conn_str = conn_dict["connection_string"]
    table_name = conn_dict["table_name"]

    service = TableServiceClient.from_connection_string(conn_str)
    table = service.get_table_client(table_name)

    rows = list(table.list_entities())
    return pd.DataFrame(rows)