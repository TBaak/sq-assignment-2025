CREATE TABLE IF NOT EXISTS member(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    age INTEGER NOT NULL,
    weight REAL NOT NULL,
    gender TEXT NOT NULL,
    streetName TEXT NOT NULL,
    houseNumber TEXT NOT NULL,
    city TEXT NOT NULL,
    zipCode TEXT NOT NULL,
    emailAddress TEXT NOT NULL,
    phoneNumber TEXT NOT NULL
)