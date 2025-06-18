from Models.BaseClasses.DatabaseModel import DatabaseModel
from Models.BaseClasses.EncryptableModel import EncryptableModel
from Models.BaseClasses.SerializeableModel import SerializeableModel


class Scooter(EncryptableModel, DatabaseModel, SerializeableModel):
    ENCRYPTED_FIELDS = [
        'brand',
        'model',
        'serial_number',
        'top_speed',
        'battery_capacity',
        'state_of_charge',
        'target_range_soc_min',
        'target_range_soc_max',
        'location_lat',
        'location_lng',
        'out_of_service_status',
        'mileage',
        'last_maintenance',
        'in_service_date'
    ]

    id: int = None
    brand: str = None
    model: str = None
    serial_number: str = None
    top_speed: str = None
    battery_capacity: str = None
    state_of_charge: str = None
    target_range_soc_min: str = None
    target_range_soc_max: str = None
    location_lat: str = None
    location_lng: str = None
    out_of_service_status: str = None
    mileage: str = None
    last_maintenance: str = None
    in_service_date: str = None
