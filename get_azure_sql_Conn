import pyodbc
import pandas as pd

def get_azure_sql_df(conn_dict):
    server = conn_dict["server"]
    database = conn_dict["database"]
    username = conn_dict["username"]
    password = conn_dict["password"]
    driver = conn_dict.get("driver", "{ODBC Driver 17 for SQL Server}")
    query = conn_dict["query_text"]

    conn_str = f"""
        DRIVER={driver};
        SERVER={server};
        DATABASE={database};
        UID={username};
        PWD={password};
        Encrypt=yes;
        TrustServerCertificate=no;
    """

    conn = pyodbc.connect(conn_str)
    df = pd.read_sql(query, conn)
    conn.close()

    return df