import time

import flet as ft

from components.chat_history import ChatHistory
from stores.chat_store import Chat
from stores.user_store import User


class ChatInput(ft.Container):
    text_field = ft.TextField(
        multiline=True,
        min_lines=1,
        max_lines=7,
        expand=True,
        border_color=ft.colors.TRANSPARENT,
        filled=True,
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        shift_enter=True,
    )

    send_button = ft.IconButton(ft.icons.SEND_ROUNDED)

    def __init__(self, page: ft.Page, chat_history: ChatHistory):
        super().__init__()
        self.page = page
        self.chat_history = chat_history
        self.author_user = chat_history.user

        self.text_field.on_submit = self.send_message
        self.send_button.on_click = self.send_message
        self.content = ft.Row(
            spacing=0,
            controls=[
                self.text_field,
                self.send_button,
            ],
        )

    def send_message(self, e: ft.ControlEvent) -> None:
        message_text = self.text_field.value
        self.text_field.disabled = True
        self.text_field.value = "..."
        self.page.update()

        message = self.chat_history.chat.add_message(author_user=self.author_user, message_text=message_text)
        self.chat_history.add_message(message)
        print(f"sending: {message_text}")

        self.text_field.disabled = False
        self.text_field.value = ""
        self.page.update()
