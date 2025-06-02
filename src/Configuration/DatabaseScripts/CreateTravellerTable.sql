CREATE TABLE IF NOT EXISTS travellers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    street_name TEXT NOT NULL,
    dob TEXT NOT NULL,
    gender TEXT NOT NULL,
    house_number TEXT NOT NULL,
    city TEXT NOT NULL,
    zip_code TEXT NOT NULL,
    email_address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    number TEXT NOT NULL,
    driving_license_number TEXT NOT NULL
)