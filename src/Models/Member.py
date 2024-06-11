from typing import Optional


class Member:

    # Member information
    id: Optional[int]
    firstName: str
    lastName: str
    age: int
    weight: int
    gender: str

    # Member address
    streetName: str
    houseNumber: int
    zipCode: str
    city: str

    # Member contact details
    phoneNumber: str
    emailAddress: str