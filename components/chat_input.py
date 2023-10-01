import time

import flet as ft


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

    def __init__(self, page):
        super().__init__()
        self.page = page
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
        message_body = self.text_field.value
        self.text_field.disabled = True
        self.text_field.value = "..."
        self.page.update()

        print(f"sending: {message_body}")

        self.text_field.disabled = False
        self.text_field.value = ""
        self.page.update()
