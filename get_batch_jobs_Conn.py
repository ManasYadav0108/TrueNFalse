from azure.batch import BatchServiceClientfrom azure.batch.batch_auth import SharedKeyCredentialsimport pandas as pd
def get_batch_jobs_df(conn_dict):
    account_name = conn_dict["account_name"]
    account_key = conn_dict["account_key"]
    batch_url = conn_dict["batch_url"]

    creds = SharedKeyCredentials(account_name, account_key)
    client = BatchServiceClient(creds, batch_url)

    jobs = list(client.job.list())
    return pd.DataFrame([job.as_dict() for job in jobs])