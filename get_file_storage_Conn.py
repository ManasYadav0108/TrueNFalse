from azure.storage.file import FileServiceimport pandas as pdfrom io import BytesIO
def get_file_storage_df(conn_dict):
    account_name = conn_dict["account_name"]
    account_key = conn_dict["account_key"]
    share_name = conn_dict["share_name"]
    file_path = conn_dict["file_path"]

    service = FileService(account_name, account_key)
    data = service.get_file_to_bytes(share_name, None, file_path).content

    return pd.read_csv(BytesIO(data))