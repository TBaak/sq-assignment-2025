CREATE TABLE IF NOT EXISTS backup_one_time_codes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    one_time_code TEXT NOT NULL,
    backup_name TEXT NOT NULL
)