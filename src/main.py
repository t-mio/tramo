import flet as ft
import flet_map as map
from data.tram_data import get_tram_data
from pages.home import HomePage
from pages.map import MapPage
from pages.tram import TramPage
from pages.location import LocationPage
from pages.schedule import SchedulePage
from pages.payment import PaymentPage
from components.bottom_nav import BottomNavigation

class MobileApp:
    def __init__(self):
        self.current_page_index = 0
        self.pages = []
        self.main_content = None
        self.bottom_nav = None

    def main(self, page: ft.Page):
        # プリロード: tram.json を起動時に一度だけ読み込んでキャッシュ
        # 以降の get_tram_data() はキャッシュ済みデータを返す
        get_tram_data()
        # アプリのタイトルを設定
        page.title = "Tramo"
        page.window.width=390
        page.window.height=844
        # ウィンドウの垂直方向の配置を中央揃えに
        page.vertical_alignment = ft.MainAxisAlignment.START
        # ウィンドウの背景色を少しグレーに
        page.bgcolor = ft.Colors.GREY_200
        page.theme_mode = ft.ThemeMode.LIGHT

        self.pages = [
            HomePage(page),
            MapPage(page),
            TramPage(page),
            LocationPage(page),
            SchedulePage(page),
            PaymentPage(page),

        ]

        self.main_content = ft.Container(
            content=self.pages[self.current_page_index].create_page(),
            expand=True,
            bgcolor=ft.Colors.WHITE
        )
        self.bottom_nav = BottomNavigation(page, self.on_nav_change)

        page.add(
            ft.Column(
                [
                    self.main_content,
                    self.bottom_nav.create_bottom_nav()
                ],
                spacing=0,
                expand=True

            )
        )
        page.update()

    def on_nav_change(self, index: int):
        if 0<= index < len(self.pages):
            self.main_content.content = self.pages[index].create_page()
            self.main_content.update()

def main():
    app = MobileApp()
    ft.app(target=app.main)


# アプリを実行
main()