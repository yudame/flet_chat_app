import flet as ft


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
        return ft.Row(
            [
                ft.TextButton(
                    "why live?", on_click=lambda x: print("talk about why live")
                ),
                ft.TextButton(
                    "am i crazy?", on_click=lambda x: print("talk about am i crazy")
                ),
                ft.TextButton(
                    "what to do?", on_click=lambda x: print("talk about what to do")
                ),
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
