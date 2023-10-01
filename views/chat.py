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
        self.appbar = AppBar(page=page)
        self.controls = [
            ChatHistory(page=page, chat=chat, user=user),
            ChatInput(page=page),
        ]
