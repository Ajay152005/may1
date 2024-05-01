import mysql.connector
from config import mysql_config

def connect():
    return mysql.connector.connect(**mysql_config)

def execute_query(query, params=None):
    conn = connect()

    cursor= conn.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return cursor
    finally:
        cursor.close()
        conn.close()

def fetch(query, params=None):
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()  # Close cursor after fetching results
    connection.commit()
    connection.close()
    return result
