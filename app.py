import json
import os
import flet as ft
from flet_core.types import AppView

from stores.chat_store import ChatStore
from stores.user_store import UserStore
from views.chat import ChatView

with open("assets/ai_config.json", "r") as f:
    os.environ["AI_CONFIG"] = json.dumps(json.loads(f.read()))
    if not all([
        "chat_topics" in os.environ["AI_CONFIG"],
        "engagement" in os.environ["AI_CONFIG"],
    ]):
        raise ValueError("AI_CONFIG is missing required keys")

def main(page: ft.Page):
    # stores
    user_store = UserStore()
    chat_store = ChatStore()

    # page setup
    page.title = "Not A Therapist"
    page.theme_mode = ft.ThemeMode.DARK

    # FIRST APP LAUNCH
    # 1. create new chat
    first_chat = chat_store.new_chat()
    # 2. start chatting
    page.views.append(
        ChatView(
            page=page,
            chat=first_chat,
            user=user_store.user,
        )
    )

    # first render
    page.update()


ft.app(
    name="Not A Therapist App by Official",
    view=AppView.FLET_APP,
    assets_dir="assets",
    upload_dir="assets/uploads",
    use_color_emoji=True,
    target=main,
),
