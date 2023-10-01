import flet as ft

from components.chat_history import ChatHistory
from components.chat_input import ChatInput
from stores.chat_store import Chat
from stores.user_store import User


class ChatView(ft.View):
    def __init__(self, page: ft.Page, chat: Chat, user: User):
        super().__init__()
        self.route = "/chat"

        self.controls = [
            ChatHistory(page=page, chat=chat, user=user),
            ft.Container(
                ft.ListView(
                    expand=1,
                    spacing=10,
                    padding=20,
                    auto_scroll=True,
                    controls=[ft.Text(f"prompt"), ft.Text(f"response")],
                )
            ),
            ChatInput(page=page),
        ]
