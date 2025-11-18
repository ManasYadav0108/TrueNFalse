from azure.search.documents import SearchClient
import pandas as pd
def get_search_df(conn_dict):
    endpoint = conn_dict["endpoint"]
    index_name = conn_dict["index_name"]
    api_key = conn_dict["api_key"]
    query = conn_dict.get("query_text", "*")
    client = SearchClient(endpoint, index_name, api_key)
    results = client.search(query)
    return pd.DataFrame([r for r in results])