from azure.datalake.store import core, lib
import pandas as pd
from io import BytesIO

def get_adls_gen1_df(conn_dict):
    tenant_id = conn_dict["tenant_id"]
    client_id = conn_dict["client_id"]
    client_secret = conn_dict["client_secret"]
    store_name = conn_dict["store_name"]
    file_path = conn_dict["file_path"]

    token = lib.auth(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
    adls = core.AzureDLFileSystem(token, store_name=store_name)

    with adls.open(file_path, 'rb') as f:
        data = f.read()

    return pd.read_csv(BytesIO(data))