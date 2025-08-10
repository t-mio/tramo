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
        number = random.randint(0,5)

        #ホーム画面の写真を表示
        background = ft.Image(
            src=f"./src/assets/"+img_list[number],
            width=float("inf"),
            height=float("inf"),
            fit=ft.ImageFit.COVER,)

        content = ft.Container(
        )

        return ft.Stack(
            [
                background,
                content
            ]
        )