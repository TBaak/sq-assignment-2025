CREATE TABLE IF NOT EXISTS scooters(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    serial_number TEXT NOT NULL,
    top_speed TEXT NOT NULL,
    battery_capacity TEXT NOT NULL,
    state_of_charge TEXT NOT NULL,
    target_range_soc_min TEXT NOT NULL,
    target_range_soc_max TEXT NOT NULL,
    location_lat TEXT NOT NULL,
    location_lng TEXT NOT NULL,
    out_of_service_status TEXT NOT NULL,
    mileage TEXT NOT NULL,
    last_maintenance TEXT NOT NULL,
    in_service_date TEXT NOT NULL
)