import psycopg2
from config.config import DB_URI as DATABASE_URL

def Connect(query, values=None, fetch=False):
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()

    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        connection.commit()

        if fetch:
            return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()
