from youtubedl.database import Connect
import inspect

create_download_status_table = """
CREATE TABLE IF NOT EXISTS download_status (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    normal_download_status BOOLEAN NOT NULL,
    playlist_download_status BOOLEAN NOT NULL
);
"""
Connect(create_download_status_table)

def save_on_off(user_id, status):
    status = status if status is not None else False
    query = f"INSERT INTO download_status (user_id) VALUES (%s, %s) ON CONFLICT (user_id) DO UPDATE SET download_status = %s RETURNING download_status;"
    result = Connect(query, (user_id, status, status), fetch=True)
    return result[0] if result else None

def get_is_on_off(user_id):
    query = f"SELECT download_status FROM download_status WHERE user_id = %s;"
    result = Connect(query, (user_id,), fetch=True)
    return result[0] if result else None
