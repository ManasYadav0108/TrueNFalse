import psycopg2
import pandas as pd
def get_postgres_df(conn_dict):
    conn = psycopg2.connect(
        host=conn_dict["host"],
        user=conn_dict["username"],
        password=conn_dict["password"],
        dbname=conn_dict["database_name"],
        port=conn_dict["port"]
    )

    df = pd.read_sql(conn_dict["query_text"], conn)
    conn.close()
    return df