import flet as ft

from components.chat_history import ChatHistory
from stores.chat_store import Message


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

        self.rail_button = ft.IconButton(ft.icons.MENU_ROUNDED)
        self.chat_history_container = chat_history
        self.author_user = chat_history.user

        self.text_field.on_submit = self.send_message
        self.send_button.on_click = self.send_message
        self.content = ft.Row(
            spacing=4,
            controls=[
                self.rail_button,
                self.text_field,
                self.send_button,
            ],
        )

    def send_message(self, e: ft.ControlEvent) -> None:
        user_message_text: str = self.text_field.value
        self.text_field.value = ""
        self.lock_input()

        # add to local datastore
        user_message: Message = self.chat_history_container.chat.add_message(
            author_user=self.author_user, message_text=user_message_text
        )
        # display on screen
        self.chat_history_container.add_message(user_message)

        # get response text from ai
        self.page.ai_store.get_next_message(chat=self.chat_history_container.chat)
        # display ai response on screen
        if self.chat_history_container.chat.messages[-1].author is not self.author_user:
            ai_message: Message = self.chat_history_container.chat.messages[-1]
            self.chat_history_container.add_message(ai_message)

        # unlock the user
        self.unlock_input()

    def lock_input(self, page_update=True):
        self.text_field.disabled = True
        self.send_button.disabled = True
        if page_update:
            self.page.update()

    def unlock_input(self, page_update=True):
        self.text_field.disabled = False
        self.send_button.disabled = False
        if page_update:
            self.page.update()
