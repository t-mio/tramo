import flet as ft
from data.tram_data import get_tram_data


class SelectStop:
    def __init__(self):
        pass

    def dropdown_changed(self, e):
        pass

    def get_options(self):
        stops = [
            {"name": "鹿児島駅前"},
            {"name": "鹿児島中央駅前"},
            {"name": "鹿児島駅前"},
        ]

        options = []
        for stop in stops:
            options.append(ft.DropdownOption(key=stop["name"]))
        return options

    def get_direction_options(self):
        # プリロード済みキャッシュから取得し、lines をそのままオプション化
        tram_data = get_tram_data()
        lines = list(tram_data.get("metadata", {}).get("lines", []))
        options = []
        for line_name in lines:
            options.append(ft.DropdownOption(key=line_name))
        return options

    def create_select_stop(self):
        return ft.Row(
            [
                ft.Dropdown(
                    editable=True,
                    options=self.get_options(),
                    on_change=self.dropdown_changed,
                ),
                ft.Dropdown(
                    editable=True,
                    options=self.get_direction_options(),
                    on_change=self.dropdown_changed,
                ),
            ]
        )
