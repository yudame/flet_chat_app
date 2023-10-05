from dataclasses import asdict, dataclass
import json
from typing import List, Set, Dict, Optional, Tuple, AbstractSet
from datetime import datetime
import flet as ft
import uuid

from stores.base_store import BaseStore
from stores.user_store import User


@dataclass(frozen=True, slots=True)
class Message:
    author: User
    message: str
    timestamp: datetime = datetime.utcnow()

    @property
    def serialized(self):
        return json.dumps(asdict(self))


class Chat:
    __slots__ = ["page", "id", "member_users", "messages"]

    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.id: str = str(uuid.uuid4())
        self.member_users: Set[User] = set()
        self.messages: List[Message] = []

    def add_message(
        self,
        author_user: User,
        message_text: str,
        timestamp: Optional[datetime] = None,
    ) -> Message:
        message = Message(
            author=author_user,
            message=message_text,
            timestamp=timestamp or datetime.utcnow(),
        )
        self.member_users.add(author_user)
        self.messages.append(message)
        return message

    def get_history(self) -> Tuple[Message, ...]:
        return tuple(self.messages)

    def get_users(self) -> AbstractSet[User]:
        return frozenset(self.member_users)

    def get_new_ai_message(self) -> Message:
        return self.add_message(author_user=self.page.ai_user, message_text="")

    @property
    def serialized(self):
        return json.dumps(
            {
                "id": self.id,
                "member_users": [user.serialized for user in self.member_users],
                "messages": [message.serialized for message in self.messages],
            }
        )


class ChatStore(BaseStore):
    __slots__ = ["chats"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # self.page is provided by the BaseStore class

        self.chats: Dict[str, Chat] = dict()
        # load chats from client storage
        chats_serialized: str = self.page.client_storage.get("user_contacts")
        if chats_serialized:
            self.chats: Dict[str, Chat] = {
                chat_dict["id"]: Chat(**chat_dict)
                for chat_dict in json.loads(chats_serialized)
            }

    def new_chat(self) -> Chat:
        chat = Chat(page=self.page)
        self.add_chat(chat)
        return chat

    def add_chat(self, chat: Chat) -> None:
        self.chats[chat.id] = chat
        # self.page.client_storage.set(
        #     "chats", json.dumps({chat.id: chat.serialized for chat in self.chats})
        # )

    def get_chat(self, chat_id: str) -> Chat:
        try:
            return self.chats[chat_id]
        except KeyError:
            raise ValueError(f"No chat found for id: {chat_id}")

    def get_chat_ids(self) -> List[str]:
        return list(self.chats.keys())
