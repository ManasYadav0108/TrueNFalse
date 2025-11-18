from azure.kusto.data import KustoConnectionStringBuilder, KustoClientimport pandas as pd
def get_kusto_df(conn_dict):
    cluster = conn_dict["cluster"]
    database = conn_dict["database"]
    client_id = conn_dict["client_id"]
    client_secret = conn_dict["client_secret"]
    tenant_id = conn_dict["tenant_id"]
    query = conn_dict["query_text"]
    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
        cluster, client_id, client_secret, tenant_id
    )
    client = KustoClient(kcsb)
    response = client.execute(database, query)
    df = response.primary_results[0].to_dataframe()
    return df