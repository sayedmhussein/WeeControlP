from abc import ABC
from typing import Final

PG_INDEX: Final[str] = "/"
PG_LOGIN = "/login"
PG_HELP = "/help"
PG_USER: Final[str] = "/user"

V2_ESSENTIAL: Final[str] = "/api/v2/essential"
V2_USER: Final[str] = "/api/v2/user"
V2_USER_AUTHENTICATION: Final[str] = "/api/v2/user/authentication"


class ClaimTypes(ABC):
    USER = "user"

class ClaimValues(ABC):
    ADMIN = "admin"
