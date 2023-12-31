import datetime
import enum
from typing import Optional
import db


class UserRole(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class UserStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    IN_ACTIVE = "IN_ACTIVE"
    BLOCKED = "BLOCKED"


class TodoType(enum.Enum):
    PERSONAL = "PERSONAL"
    WORK = "WORK"
    STUDY = "STUDY"


class User:
    def __init__(self, username: str,
                 password: str,
                 id: Optional[int] = None,
                 status: Optional[UserStatus] = None,
                 role: Optional[UserRole] = None,
                 login_try_count: Optional[int] = None
                 ):
        self.id = id or db.get_user_id()
        self.username = username
        self.password = password
        self.status = status or UserStatus.IN_ACTIVE.value
        self.role = role or UserRole.USER.value
        self.login_try_count = login_try_count or 0

    @classmethod
    def from_tuple(cls, args):
        return cls(id=args[0],
                   username=args[1],
                   password=args[2],
                   status=args[3],
                   role=args[4],
                   login_try_count=args[5]
                   )

    def __repr__(self):
        return f"{self.username}:{self.status}:{self.role}"


class Todo:
    def __init__(self, name: str, user_id, type: TodoType, completed=None, id=None):
        self.id = id or db.get_todo_id()
        self.name = name
        self.type = type
        self.user_id = user_id
        self.completed = completed or False

    @classmethod
    def from_tuple(cls, agrs):
        return cls(id=agrs[0], name=agrs[1], type=agrs[2], completed=agrs[3], user_id=agrs[4])

    def __repr__(self):
        return f"Todo ID: {self.id}\n Title: {self.name}\n Type: {self.type}\n Completed: {['No', 'Yes'][self.completed]}"
