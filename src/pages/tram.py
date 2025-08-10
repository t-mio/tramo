import flet as ft

from components.select_stop import SelectStop


class TramPage:
    def __init__(self, page: ft.Page):
        self.page = page

    def create_page(self):
        content = ft.Container(
            content=SelectStop().create_select_stop()
        )

        return ft.Stack(
            [
                content
            ]
        )