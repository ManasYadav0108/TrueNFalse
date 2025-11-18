import pandas as pd
from pymongo import MongoClient

def get_cosmos_mongo_df(conn_dict):
    connection_string = conn_dict["connection_string"]
    database_name = conn_dict["database_name"]
    collection_name = conn_dict["collection_name"]
    filter_query = conn_dict.get("filter", {})

    client = MongoClient(connection_string)
    db = client[database_name]
    col = db[collection_name]

    data = list(col.find(filter_query))
    return pd.DataFrame(data)