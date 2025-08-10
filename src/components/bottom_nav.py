import flet as ft


class BottomNavigation:
    def __init__(self, page:ft.Page, on_tap_callback=None):
        self.page = page
        self.on_tap_callback = on_tap_callback
        self.current_index = 0

    def create_bottom_nav(self):

        return ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME,
                    label="ホーム"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.LOCATION_ON,
                    label="位置情報"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.TRAM,
                    label="接近情報"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.MAP,
                    label="歴史"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.SCHEDULE,
                    label="時刻表"
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PAYMENT,
                    label="運賃・乗車券"
                ),
            ],
            on_change=self._on_nav_change
        )
    
    def _on_nav_change(self, e):
        self.current_index = e.control.selected_index
        if self.on_tap_callback:
            self.on_tap_callback(self.current_index)
    
    def set_selected_index(self, index: int):
        self.current_index = index