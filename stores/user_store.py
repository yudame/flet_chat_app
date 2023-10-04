from dataclasses import dataclass, replace
from datetime import datetime
from typing import Optional, Set
import uuid


@dataclass(frozen=True, slots=True)
class User:
    id: str
    username: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime = datetime.utcnow()


class UserStore:
    __slots__ = ["user", "contacts"]

    def __init__(self, username: str = None, email: str = None):
        user_id = str(uuid.uuid4())
        user_contacts: Set[User] = set()
        self.user: User = User(id=user_id, username=username, email=email)

    def update_username(self, new_username: str) -> None:
        self.user = replace(self.user, username=new_username)

    def update_email(self, new_email: str) -> None:
        self.user = replace(self.user, email=new_email)
