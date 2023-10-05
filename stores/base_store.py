from abc import ABC
import flet as ft


class BaseStore(ABC):
    def __init__(self, page: ft.Page, *args, **kwargs):
        self.page: ft.Page = page
