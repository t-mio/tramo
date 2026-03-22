import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from theme import BG, WHITE, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY, PRIMARY_LIGHT, GOLD, BORDER, GREY, LINE1, LINE2


class PaymentPage:
    def __init__(self, page: ft.Page):
        self.page = page

    def _open_url(self, url):
        self.page.launch_url(url)

    def _create_section_title(self, title: str):
        return ft.Container(
            content=ft.Text(title, size=13, color=TEXT_SECONDARY, weight=ft.FontWeight.W_600),
            padding=ft.padding.only(top=16, bottom=8),
        )

    def _create_fare_table(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("運賃表", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Container(height=8),
                # ヘッダー
                ft.Container(
                    content=ft.Row([
                        ft.Container(ft.Text("区分", size=13, weight=ft.FontWeight.BOLD, color=WHITE), expand=2, alignment=ft.alignment.center),
                        ft.Container(ft.Text("大人", size=13, weight=ft.FontWeight.BOLD, color=WHITE), expand=1, alignment=ft.alignment.center),
                        ft.Container(ft.Text("小児", size=13, weight=ft.FontWeight.BOLD, color=WHITE), expand=1, alignment=ft.alignment.center),
                    ]),
                    bgcolor=PRIMARY,
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    border_radius=ft.border_radius.only(top_left=8, top_right=8),
                ),
                # 行
                *[
                    ft.Container(
                        content=ft.Row([
                            ft.Container(ft.Text(row[0], size=13, color=TEXT_PRIMARY), expand=2, alignment=ft.alignment.center_left, padding=ft.padding.only(left=12)),
                            ft.Container(ft.Text(row[1], size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD), expand=1, alignment=ft.alignment.center),
                            ft.Container(ft.Text(row[2], size=13, color=TEXT_PRIMARY, weight=ft.FontWeight.BOLD), expand=1, alignment=ft.alignment.center),
                        ]),
                        bgcolor=WHITE if i % 2 == 0 else PRIMARY_LIGHT,
                        padding=ft.padding.symmetric(vertical=10),
                        border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
                    )
                    for i, row in enumerate([
                        ("均一運賃（現金）", "170円", "90円"),
                        ("均一運賃（ラピカ）", "170円", "90円"),
                        ("1日乗車券（市電）", "600円", "300円"),
                        ("1日乗車券（市電・市バス）", "800円", "400円"),
                    ])
                ],
            ]),
            bgcolor=WHITE,
            border=ft.border.all(1, BORDER),
            border_radius=8,
            margin=ft.margin.only(bottom=8),
        )

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

    def _create_howto_card(self):
        steps = [
            ("1", "後ろのドアから乗車する"),
            ("2", "整理券は不要（均一運賃のため）"),
            ("3", "前のドアから降車する"),
            ("4", "降車時に運賃箱へ支払い"),
        ]
        return ft.Container(
            content=ft.Column([
                ft.Text("乗車方法", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Container(height=8),
                *[
                    ft.Row([
                        ft.Container(
                            content=ft.Text(step[0], color=WHITE, size=13, weight=ft.FontWeight.BOLD),
                            width=28, height=28,
                            bgcolor=PRIMARY,
                            border_radius=14,
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(step[1], size=13, color=TEXT_PRIMARY, expand=True),
                    ], spacing=12)
                    for step in steps
                ],
            ], spacing=10),
            padding=ft.padding.all(15),
            bgcolor=WHITE,
            border=ft.border.all(1, BORDER),
            border_radius=10,
            margin=ft.margin.only(bottom=8),
        )

    def create_page(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "運賃・乗車券",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=WHITE,
                        ),
                        padding=ft.padding.symmetric(horizontal=20, vertical=14),
                        bgcolor=PRIMARY,
                    ),
                    ft.Container(
                        content=ft.Column([
                            self._create_section_title("運賃表"),
                            self._create_fare_table(),
                            self._create_section_title("乗車方法"),
                            self._create_howto_card(),
                            self._create_section_title("乗車券・ICカード"),
                            self._create_link_card(
                                ft.Icons.CREDIT_CARD,
                                "ラピカ（ICカード）",
                                "チャージ・利用方法の案内",
                                "https://www.kotsu-city-kagoshima.jp/ticket-summary/rapica/",
                                color="#1B5E20",
                            ),
                            self._create_link_card(
                                ft.Icons.CONFIRMATION_NUMBER,
                                "一日乗車券",
                                "スマホ一日乗車券・紙券の案内",
                                "https://www.kotsu-city-kagoshima.jp/ticket-summary/oneday/",
                                color="#E65100",
                            ),
                            self._create_link_card(
                                ft.Icons.CARD_MEMBERSHIP,
                                "定期券",
                                "定期券の種類・購入方法",
                                "https://www.kotsu-city-kagoshima.jp/ticket-summary/coupon/",
                                color="#4A148C",
                            ),
                        ]),
                        padding=ft.padding.all(16),
                        expand=True,
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
            ),
            bgcolor=BG,
            expand=True,
        )