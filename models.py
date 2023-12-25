import enum
from typing import Optional


class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class UserStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    IN_ACTIVE = "IN_ACTIVE"
    BLOCKED = "BLOCKED"


class User:
    def __init__(self, id: int,
                 username: str,
                 password: str,
                 status: Optional[UserStatus],
                 role: Optional[UserRole],
                 login_try_count: Optional[int]):
        self.id = id
        self.username = username
        self.password = password
        self.status = status or UserStatus.ACTIVE.value
        self.role = role or UserRole.USER.value
        self.login_try_count = login_try_count or 0

    @classmethod
    def from_tuple(cls, args):
        return cls(
            id=args[0],
            username=args[1],
            password=args[2],
            status=args[3],
            role=args[4],
            login_try_count=args[5]
        )
