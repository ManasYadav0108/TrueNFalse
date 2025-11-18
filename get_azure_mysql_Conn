def get_azure_mysql_Conn(conn_dict):

    # Extract credentials from the dictionary
    host = conn_dict.get("host")
    database = conn_dict.get("database_name")
    username = conn_dict.get("username")
    password = conn_dict.get("password")
    port = conn_dict.get("port")
    query_text = conn_dict.get("query_text")

    # Connect to Azure MySQL
    db = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database,
        port=port
    )

    # Fetch the data
    df = pd.read_sql(query_text, con=db)
    db.close()

    return df
