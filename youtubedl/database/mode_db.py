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
    normal_status = normal_status if normal_status is not None else False
    query = """
    INSERT INTO download_status (user_id, normal_download_status, playlist_download_status) 
    VALUES (%s, %s, %s) 
    ON CONFLICT (user_id) 
    DO UPDATE SET normal_download_status = COALESCE(%s, download_status.normal_download_status),
                  playlist_download_status = COALESCE(%s, download_status.playlist_download_status)
    RETURNING normal_download_status, playlist_download_status;
    """
    result = Connect(query, (user_id, normal_status, playlist_status, normal_status, playlist_status), fetch=True)
    return result[0] if result else None


def get_is_on_off(user_id, mode=None):
    if mode == "nrml":
        query = "SELECT normal_download_status FROM download_status WHERE user_id = %s;"
    elif mode == "playlist":
        query = "SELECT playlist_download_status FROM download_status WHERE user_id = %s;"
    else:
        query = "SELECT normal_download_status, playlist_download_status FROM download_status WHERE user_id = %s;"
    result = Connect(query, (user_id,), fetch=True)
    if result and len(result[0]) == 1:
        return result[0][0]
    elif result and len(result[0]) == 2:
        return result[0]
    return None
