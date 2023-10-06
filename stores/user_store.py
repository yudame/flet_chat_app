from dataclasses import asdict, dataclass, replace
from datetime import datetime
import json
import logging
from typing import Optional, Set
import uuid

from stores.base_store import BaseStore


@dataclass(slots=True)
class User:
    id: str
    name: str = "Human"
    handle: Optional[str] = None
    created_at: datetime = datetime.utcnow()

    @property
    def serialized(self):
        return json.dumps(asdict(self))


class UserStore(BaseStore):
    __slots__ = ["page", "user", "contacts"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.page is provided by the BaseStore class

        # load user info from client storage
        self.user = None
        user_serialized: str = self.page.client_storage.get("user")
        if user_serialized:
            try:
                self.user = User(**json.loads())
                self.page.client_storage.set("user", self.user.serialized)
            except:
                logging.exception(
                    f"Failed to load user. user_serialized: {user_serialized}"
                )
        if not self.user:
            self.user = User(id=str(uuid.uuid4()))

        # load contacts from client storage
        self.user_contacts: Set[User] = set()
        user_contacts_serialized: str = self.page.client_storage.get("user_contacts")
        if user_contacts_serialized:
            self.user_contacts: Set[User] = set(
                [
                    User(**user_dict)
                    for user_dict in json.loads(user_contacts_serialized)
                ]
            )

    def update_user_attr(self, attr, value):
        self.user = replace(self.user, **{attr: value})
        self.page.client_storage.set("user", self.user.serialized)
        self.page.update()
