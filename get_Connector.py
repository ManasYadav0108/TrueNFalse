import pandas as pd
from azure.kusto.data import KustoConnectionStringBuilder, KustoClient
from flask import Flask, request
from utility import get_connection

# from connectors.kusto_connector import get_kusto_df
# from connectors.mysql_connector import get_mysql_df
# from connectors.postgres_connector import get_postgres_df
# from connectors.table_storage_connector import get_table_storage_df
# from connectors.eventhub_connector import get_eventhub_df
# from connectors.search_connector import get_search_df
# from connectors.batch_connector import get_batch_jobs_df
# from connectors.keyvault_connector import get_keyvault_secret
# from connectors.sqlserver_connector import get_sqlserver_df
# from connectors.adls_connector import get_adls_df   # your original



def get_kusto_df(dataSet):
    """
    connector_name: name of the row in connector_kusto table
    mysql_conn: active MySQL DB connection (mysql.connector.connect)
    """

    # -------------------------------------------------
    # 1. Fetch Kusto credentials from MySQL
    # -------------------------------------------------
    conn = mysql_conn.cursor(dictionary=True)

    conn.execute("""
        SELECT cluster_url, database_name, query_text,
               client_id, client_secret, authority_id
        FROM connector_kusto
        WHERE name = %s
    """, (connector_name,))

    creds = conn.fetchone()

    if not creds:
        raise Exception(f"No Azure Data Explorer config found for '{connector_name}'")

    # -------------------------------------------------
    # 2. Create Kusto Connection Builder
    # -------------------------------------------------
    kcsb = KustoConnectionStringBuilder.with_aad_application_key_authentication(
        creds["cluster_url"],
        creds["client_id"],
        creds["client_secret"],
        creds["authority_id"]
    )

    client = KustoClient(kcsb)

    # -------------------------------------------------
    # 3. Execute query from MySQL configuration
    # -------------------------------------------------
    result = client.execute(
        database=creds["database_name"],
        query=creds["query_text"]
    )

    # Convert table to pandas DataFrame
    df = result.primary_results[0].to_dataframe()

    return df




def get_azure_mysql_df(connector_name, mysql_conn):
    conn = mysql_conn.cursor(dictionary=True)
    conn.execute("""
        SELECT host, database_name, username, password, port, query_text
        FROM connector_azure_mysql
        WHERE name=%s
    """, (connector_name,))
    creds = conn.fetchone()
    conn.close()

    db = mysql.connector.connect(
        host=creds["host"],
        user=creds["username"],
        password=creds["password"],
        database=creds["database_name"],
        port=creds["port"]
    )

    df = pd.read_sql(creds["query_text"], con=db)
    db.close()
    return df




app = Flask(__name__)

def read_source(source):

    conn  = get_connection()

    connectors = {  
        "kusto": get_kusto_df,
        "mysql": get_mysql_df,
        "postgres": get_postgres_df,
        "table": get_table_storage_df,
        "eventhub": get_eventhub_df,
        "search": get_search_df,
        "batch": get_batch_jobs_df,
        "keyvault": get_keyvault_secret,
        "sqlserver": get_sqlserver_df,
        "adls": get_adls_df
    }

    if source not in connectors:
        return {"error": "Invalid source"}, 400
    df = connectors[source](dataSet)

    if not hasattr(df, "to_json"):  # Key Vault returns string
        return {"value": df}

    return df.to_json(orient="records")


if __name__ == "__main__":
    app.run(debug=True)