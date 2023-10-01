import flet as ft

from components.appbar import AppBar
from components.chat_history import ChatHistory
from components.chat_input import ChatInput
from stores.chat_store import Chat
from stores.user_store import User


class ChatView(ft.View):
    def __init__(self, page: ft.Page, chat: Chat, user: User):
        super().__init__()
        self.route = "/chat"
        self.chat = chat
        self.user = user

        # COMPONENTS
        chat_history = ChatHistory(page=page, chat=chat, user=user)
        chat_input = ChatInput(page=page, chat_history=chat_history)

        # UI
        self.appbar = AppBar(page=page)
        self.controls = [
            chat_history,
            chat_input,
        ]
