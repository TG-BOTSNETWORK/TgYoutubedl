from youtubedl.database import Connect

create_download_status_table = """
CREATE TABLE IF NOT EXISTS download_status (
    id SERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    normal_download_status BOOLEAN NOT NULL,
    playlist_download_status BOOLEAN NOT NULL
);
"""
Connect(create_download_status_table)

def save_on_off(user_id, status, mode):
    column_name = f"{mode}_download_status"
    query = f"INSERT INTO download_status (user_id, {column_name}) VALUES (%s, COALESCE(%s, FALSE)) ON CONFLICT (user_id) DO UPDATE SET {column_name} = COALESCE(%s, FALSE) RETURNING {column_name};"
    result = Connect(query, (user_id, status, status), fetch=True)
    return result[0] if result else None


def get_is_on_off(user_id, mode):
    column_name = f"{mode}_download_status"
    query = f"SELECT {column_name} FROM download_status WHERE user_id = %s;"
    result = Connect(query, (user_id,), fetch=True)
    return result[0] if result else None
