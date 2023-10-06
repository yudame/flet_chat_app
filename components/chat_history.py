import flet as ft

from stores.chat_store import Chat, Message
from stores.user_store import User


class ChatHistory(ft.Container):
    messages_list = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    def __init__(self, page: ft.Page, chat: Chat, user: User):
        super().__init__()
        self.page = page
        self.chat = chat
        self.user = user
        self.load_messages()

        self.content = self.messages_list
        self.expand = 1

    def load_messages(self) -> None:
        for message in self.chat.get_message_history():
            self.add_message(message)
        self.page.update()

    def add_message(self, message: Message, update_page: bool = True) -> None:
        if message.author is self.user:
            self.messages_list.controls.append(
                ft.Text(
                    message.message,
                    text_align=ft.TextAlign.RIGHT,
                    color="blue",
                )
            )
        else:
            self.messages_list.controls.append(
                ft.Text(
                    message.message,
                    text_align=ft.TextAlign.LEFT,
                )
            )

        if update_page:
            self.page.update()
