from enum import Enum


class LoginError(Enum):
    NotFound = "not_found"
    BadCredentials = "bad_credentials"
