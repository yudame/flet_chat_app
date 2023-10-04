from dataclasses import dataclass
from typing import List, Set, Dict, Optional, Tuple, AbstractSet
from datetime import datetime
import uuid
from stores.user_store import User


@dataclass(frozen=True, slots=True)
class Message:
    author: User
    message: str
    timestamp: datetime = datetime.utcnow()


class Chat:
    __slots__ = ["id", "member_users", "history"]

    def __init__(self):
        self.id: str = str(uuid.uuid4())
        self.member_users: Set[User] = set()
        self.history: List[Message] = []

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
        self.history.append(message)
        return message

    def get_history(self) -> Tuple[Message, ...]:
        return tuple(self.history)

    def get_users(self) -> AbstractSet[User]:
        return frozenset(self.member_users)

    def get_new_ai_message(self) -> Message:
        return self.add_message(author_user=_)



class ChatStore:
    __slots__ = ["chats"]

    def __init__(self):
        self.chats: Dict[str, Chat] = {}

    def new_chat(self) -> Chat:
        chat = Chat()
        self.chats[chat.id] = chat
        return chat

    def add_chat(self, chat: Chat) -> None:
        self.chats[chat.id] = chat

    def get_chat(self, chat_id: str) -> Chat:
        try:
            return self.chats[chat_id]
        except KeyError:
            raise ValueError(f"No chat found for id: {chat_id}")

    def get_chat_ids(self) -> List[str]:
        return list(self.chats.keys())
