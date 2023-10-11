import flet as ft
from flet_core.types import AppView

from settings.settings import APP_CONFIG
from stores.chat_store import ChatStore
from stores.user_store import UserStore
from stores.ai_store import AIStore
from views.chat import ChatView


def main(page: ft.Page):
    # add storages
    page.user_store = UserStore(page=page)
    page.chat_store = ChatStore(page=page)
    page.ai_store = AIStore(page=page)

    page.title = APP_CONFIG["title"]
    page.theme_mode = ft.ThemeMode.DARK

    # FIRST APP LAUNCH
    # 1. create new chat
    first_chat = page.chat_store.new_chat()
    # 2. start chatting
    page.views.append(
        ChatView(
            page=page,
            chat=first_chat,
            user=page.user_store.user,
        )
    )

    # first render
    page.update()


ft.app(
    name=APP_CONFIG["name"],
    view=AppView.FLET_APP,
    assets_dir=APP_CONFIG["assets_dir"],
    upload_dir=APP_CONFIG["upload_dir"],
    use_color_emoji=True,
    target=main,
),
