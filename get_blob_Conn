from azure.storage.blob import BlobServiceClient
import pandas as pd
from io import BytesIO

def get_blob_df(conn_dict):
    account_url = conn_dict["account_url"]
    container_name = conn_dict["container_name"]
    blob_name = conn_dict["blob_name"]
    credential = conn_dict["credential"]  # SAS token or key

    blob_service = BlobServiceClient(account_url, credential=credential)
    blob_client = blob_service.get_blob_client(container_name, blob_name)
    data = blob_client.download_blob().readall()

    return pd.read_csv(BytesIO(data))