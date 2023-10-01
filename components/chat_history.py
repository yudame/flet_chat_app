import flet as ft

from stores.chat_store import Chat
from stores.user_store import User


class ChatHistory(ft.Container):
    messages_list = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    def __init__(self, page: ft.Page, chat: Chat, user: User):
        super().__init__()
        self.page = page

        # for message in chat.get_history():
        #     if message.author is user:
        #         self.messages_list.controls.append(
        #             ft.Text(
        #                 message.message,
        #                 text_align=ft.TextAlign.RIGHT,
        #                 color="blue",
        #             )
        #         )
        #     else:
        #         self.messages_list.controls.append(
        #             ft.Text(
        #                 message.message,
        #                 text_align=ft.TextAlign.LEFT,
        #             )
        #         )

        for i in range(0, 5):
            self.messages_list.controls.append(
                ft.Text(f"prompt {i + 1}", text_align=ft.TextAlign.RIGHT, color="blue")
            )
            self.messages_list.controls.append(ft.Text(f"response {i + 1}"))

        self.content = self.messages_list
