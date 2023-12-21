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

def save_on_off(user_id, normal_status=None, playlist_status=None):
    normal_status = normal_status if normal_status is not None else get_is_on_off(user_id)
    playlist_status = playlist_status if playlist_status is not None else get_is_on_off(user_id, playlist=True)

    query = """
    INSERT INTO download_status (user_id, normal_download_status, playlist_download_status) 
    VALUES (%s, %s, %s) 
    ON CONFLICT (user_id) 
    DO UPDATE SET normal_download_status = %s, playlist_download_status = %s 
    RETURNING normal_download_status, playlist_download_status;
    """

    result = Connect(query, (user_id, normal_status, playlist_status, normal_status, playlist_status), fetch=True)
    return result[0] if result else None

def get_is_on_off(user_id, playlist=False):
    column = "playlist_download_status" if playlist else "normal_download_status"
    query = f"SELECT {column} FROM download_status WHERE user_id = %s;"
    result = Connect(query, (user_id,), fetch=True)
    return result[0] if result else None
