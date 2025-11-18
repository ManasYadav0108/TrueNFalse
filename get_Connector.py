import pandas as pd
from azure.kusto.data import KustoConnectionStringBuilder, KustoClient
from flask import Flask, request
from utility import get_connection

def read_source(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Fetch connection details as a dictionary
    cursor.execute("""
        SELECT *
        FROM connectors
        WHERE id = %s
    """, (id,))
    
    conn_dict = cursor.fetchone()   # ← This is now a Python dictionary
    cursor.close()
    conn.close()

    if not conn_dict:
        return {"error": "Invalid ID"}, 404

    # 2. Get the source type from the dictionary row
    source = conn_dict["source"]

    # 3. List of connector functions
    connectors = {  
        "kusto": get_kusto_Conn,
        "mysql": get_mysql_Conn,
        "postgres": get_postgres_Conn,
        "table": get_table_storage_Conn,
        "eventhub": get_eventhub_Conn,
        "search": get_search_Conn,
        "batch": get_batch_jobs_Conn,
        "keyvault": get_keyvault_secret,
        "sqlserver": get_sqlserver_Conn,
        "adls": get_adls_Conn
    }

    # 4. Validate source
    if source not in connectors:
        return {"error": "Invalid source"}, 400

    # 5. Call the correct connector function and pass dictionary
    df = connectors[source](conn_dict)

    # 6. KeyVault returns string → no "to_json"
    if not hasattr(df, "to_json"):
        return {"value": df}

    return df.to_json(orient="records")
