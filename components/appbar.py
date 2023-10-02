import flet as ft
import json
import os

class AppBar(ft.AppBar):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.leading = ft.Icon(ft.icons.HEALTH_AND_SAFETY_ROUNDED)
        self.leading_width = 60
        self.title = self.get_title()
        self.center_title = False
        self.bgcolor = ft.colors.BLACK54
        self.actions = self.get_actions()

    def get_title(self):
        topics = list(json.loads(os.environ.get("AI_CONFIG", "{}")).get("chat_topics", {}).keys())
        return ft.Row(
            [
                ft.TextButton(
                    topic_category.title(), on_click=lambda _: print(f"talk about {str(topic_category)}")
                ) for topic_category in topics
            ]
        )

    def get_actions(self):
        def get_actions():
            return (
                [
                    # ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),  # to change theme light/dark
                    ft.IconButton(
                        ft.icons.RESTART_ALT_ROUNDED,
                        on_click=lambda x: print("reset app"),
                    ),
                ],
            )
