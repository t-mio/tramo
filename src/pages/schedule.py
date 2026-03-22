import flet as ft
import sys
from pathlib import Path

_src_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_src_dir))

from theme import BG, WHITE, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY, PRIMARY_LIGHT, GOLD, BORDER, LINE1, LINE2


class SchedulePage:
    def __init__(self, page: ft.Page):
        self.page = page

    def _open_url(self, url):
        self.page.launch_url(url)

    def _create_link_card(self, icon, title, subtitle, url, color=None):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=WHITE, size=22),
                    width=44,
                    height=44,
                    bgcolor=color or PRIMARY,
                    border_radius=8,
                    alignment=ft.alignment.center,
                ),
                ft.Column([
                    ft.Text(title, size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                    ft.Text(subtitle, size=12, color=TEXT_SECONDARY),
                ], spacing=2, expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT, color=TEXT_SECONDARY),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12),
            padding=ft.padding.all(15),
            bgcolor=WHITE,
            border=ft.border.all(1, BORDER),
            border_radius=10,
            margin=ft.margin.only(bottom=8),
            on_click=lambda e, u=url: self._open_url(u),
            ink=True,
        )

    def create_page(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "運行情報",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=WHITE,
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=14),
                        bgcolor=PRIMARY,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Container(
                                content=ft.Text("運行状況", size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                                padding=ft.padding.only(bottom=8),
                            ),
                            self._create_link_card(
                                ft.Icons.TRAIN,
                                "運行状況 遅延情報",
                                "Yahoo!路線情報",
                                "https://transit.yahoo.co.jp/diainfo/619/0",
                            ),
                            self._create_link_card(
                                ft.Icons.LANGUAGE,
                                "鹿児島市交通局 公式サイト",
                                "運行状況・お知らせ",
                                "https://www.kotsu-city-kagoshima.jp/",
                            ),
                            ft.Container(
                                content=ft.Text("お知らせ", size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                                padding=ft.padding.only(top=16, bottom=8),
                            ),
                            self._create_link_card(
                                ft.Icons.NOTIFICATIONS,
                                "お知らせ一覧",
                                "最新のお知らせを確認する",
                                "https://www.kotsu-city-kagoshima.jp/topics/",
                            ),
                            ft.Container(
                                content=ft.Text("SNS・問い合わせ", size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                                padding=ft.padding.only(top=16, bottom=8),
                            ),
                            self._create_link_card(
                                ft.Icons.TAG,
                                "公式X（旧Twitter）",
                                "@kago_city_ko2",
                                "https://twitter.com/kago_city_ko2",
                                color="#000000",
                            ),
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("お問い合わせ先", size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
                                    ft.Container(height=8),
                                    ft.Row([
                                        ft.Icon(ft.Icons.PHONE, color=PRIMARY, size=18),
                                        ft.Column([
                                            ft.Text("電車事業課", size=13, color=TEXT_PRIMARY),
                                            ft.Text("099-257-2116", size=15, weight=ft.FontWeight.BOLD, color=PRIMARY),
                                        ], spacing=1),
                                    ], spacing=10),
                                ]),
                                padding=ft.padding.all(15),
                                bgcolor=PRIMARY_LIGHT,
                                border_radius=10,
                                margin=ft.margin.only(top=8),
                            ),
                        ]),
                        padding=ft.padding.all(16),
                        expand=True,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=BG,
            expand=True,
        )