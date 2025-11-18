from azure.storage.filedatalake import DataLakeServiceClient
import pandas as pd
from io import BytesIO

def get_adls_gen2_df(conn_dict):
    account_url = conn_dict["account_url"]
    file_system = conn_dict["file_system"]
    file_path = conn_dict["file_path"]
    credential = conn_dict["credential"]

    service = DataLakeServiceClient(account_url, credential=credential)
    file_client = service.get_file_client(file_system, file_path)

    data = file_client.download_file().readall()
    return pd.read_csv(BytesIO(data))