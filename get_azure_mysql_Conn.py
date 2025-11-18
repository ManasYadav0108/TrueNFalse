def get_mysql_df(conn_dict):
    db = mysql.connector.connect(
        host=conn_dict["host"],
        user=conn_dict["username"],
        password=conn_dict["password"],
        database=conn_dict["database_name"],
        port=conn_dict["port"]
    )

    df = pd.read_sql(conn_dict["query_text"], con=db)
    db.close()

    return df