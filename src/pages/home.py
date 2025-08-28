import flet as ft
import random

class HomePage:
    def __init__(self, page: ft.Page):
        self.page = page

    def create_page(self):
        img_list = [
            "city-tram.jpeg",
            "kiriko.jpeg",
            "hanadennsha.jpg",
            "kiriko nakami.jpeg",
            "siden1.jpeg",
            "teisho1.jpeg"
        ]
        number = random.randint(0, len(img_list) - 1)
        filename = img_list[number]

        # assets_dir が設定されているため `src=filename` で解決される
        background = ft.Image(
            src=filename,
            width=float("inf"),
            height=float("inf"),
            fit=ft.ImageFit.COVER,
        )

        content = ft.Container(
        )

        return ft.Stack(
            [
                background,
                content
            ]
        )