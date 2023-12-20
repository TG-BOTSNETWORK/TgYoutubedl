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


create_download_status_table = """
CREATE TABLE IF NOT EXISTS download_status (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    normal_download_status BOOLEAN NOT NULL,
    playlist_download_status BOOLEAN NOT NULL
);
"""
Connect(create_download_status_table)

def set_normal_download_status(user_id, status):
    query = "INSERT INTO download_status (user_id, normal_download_status, playlist_download_status) VALUES (%s, %s, false) ON CONFLICT (user_id) DO UPDATE SET normal_download_status = %s RETURNING id;"
    result = Connect(query, (user_id, "on" in status, "on" in status), fetch=True)
    return result[0][0] if result else None

def set_playlist_download_status(user_id, status):
    query = "INSERT INTO download_status (user_id, normal_download_status, playlist_download_status) VALUES (%s, false, %s) ON CONFLICT (user_id) DO UPDATE SET playlist_download_status = %s RETURNING id;"
    result = Connect(query, (user_id, "on" in status, "on" in status), fetch=True)
    return result[0][0] if result else None

