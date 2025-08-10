import flet as ft


class LocationPage:
    def __init__(self, page: ft.Page):
        self.page = page

    def create_page(self):
        content = ft.Container(
        )

        return ft.Stack(
            [
                content
            ]
        )