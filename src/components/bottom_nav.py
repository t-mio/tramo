import flet as ft
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from theme import *


class BottomNavigation:
    def __init__(self, page: ft.Page, on_tap_callback=None):
        self.page = page
        self.on_tap_callback = on_tap_callback
        self.current_index = 0

    def create_bottom_nav(self):
        return ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="ホーム"),
                ft.NavigationBarDestination(icon=ft.Icons.MAP, label="路線図"),
                ft.NavigationBarDestination(icon=ft.Icons.TRAM, label="時刻表"),
                ft.NavigationBarDestination(icon=ft.Icons.SCHEDULE, label="運行情報"),
                ft.NavigationBarDestination(icon=ft.Icons.PAYMENT, label="運賃"),
            ],
            bgcolor=WHITE,
            indicator_color=PRIMARY_LIGHT,
            label_behavior=ft.NavigationBarLabelBehavior.ALWAYS_SHOW,
            on_change=self._on_nav_change,
        )

    def _on_nav_change(self, e):
        self.current_index = e.control.selected_index
        if self.on_tap_callback:
            self.on_tap_callback(self.current_index)

    def set_selected_index(self, index: int):
        self.current_index = index