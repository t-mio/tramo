import flet as ft
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from theme import BG, WHITE, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY, PRIMARY_LIGHT, GOLD, BORDER, GREY, LINE1, LINE2
from utils.timetable_data import TimetableDataManager
from utils.time_utils import get_current_time
from components.train_card import create_train_list

STOP_INFO = {
    "鹿児島駅前":           {"lines": [1, 2], "terminal": "only_down"},
    "桜島桟橋通":           {"lines": [1, 2], "terminal": None},
    "水族館口":             {"lines": [1, 2], "terminal": None},
    "市役所前":             {"lines": [1, 2], "terminal": None},
    "朝日通":               {"lines": [1, 2], "terminal": None},
    "いづろ通":             {"lines": [1, 2], "terminal": None},
    "天文館通":             {"lines": [1, 2], "terminal": None},
    "高見馬場":             {"lines": [1, 2], "terminal": None},
    "甲東中学校前":         {"lines": [1],    "terminal": None},
    "新屋敷":               {"lines": [1],    "terminal": None},
    "武之橋":               {"lines": [1],    "terminal": None},
    "二中通（キラメキテラス前）": {"lines": [1], "terminal": None},
    "荒田八幡":             {"lines": [1],    "terminal": None},
    "騎射場":               {"lines": [1],    "terminal": None},
    "鴨池":                 {"lines": [1],    "terminal": None},
    "郡元":                 {"lines": [1, 2], "terminal": None},
    "涙橋":                 {"lines": [1],    "terminal": None},
    "南鹿児島駅前":         {"lines": [1],    "terminal": None},
    "二軒茶屋":             {"lines": [1],    "terminal": None},
    "宇宿一丁目":           {"lines": [1],    "terminal": None},
    "脇田":                 {"lines": [1],    "terminal": None},
    "笹貫":                 {"lines": [1],    "terminal": None},
    "上塩屋":               {"lines": [1],    "terminal": None},
    "谷山":                 {"lines": [1],    "terminal": "only_up"},
    "加治屋町":             {"lines": [2],    "terminal": None},
    "高見橋":               {"lines": [2],    "terminal": None},
    "鹿児島中央駅前":       {"lines": [2],    "terminal": None},
    "都通":                 {"lines": [2],    "terminal": None},
    "中洲通":               {"lines": [2],    "terminal": None},
    "市立病院前":           {"lines": [2],    "terminal": None},
    "神田（交通局前）":     {"lines": [2],    "terminal": None},
    "唐湊":                 {"lines": [2],    "terminal": None},
    "工学部前":             {"lines": [2],    "terminal": None},
    "純心学園前":           {"lines": [2],    "terminal": None},
    "中郡":                 {"lines": [2],    "terminal": "only_up"},
}


def get_direction_options(stop: str):
    info = STOP_INFO.get(stop, {"lines": [1, 2], "terminal": None})
    lines = info["lines"]
    terminal = info["terminal"]

    if terminal == "only_down":
        if lines == [1]:
            return [("下り", "谷山 方面")]
        elif lines == [2]:
            return [("下り", "郡元 方面")]
        else:
            return [("下り", "谷山／郡元 方面")]
    elif terminal == "only_up":
        return [("上り", "鹿児島駅前 方面")]
    else:
        if lines == [1]:
            return [
                ("上り", "鹿児島駅前 方面"),
                ("下り", "谷山 方面"),
            ]
        elif lines == [2]:
            return [
                ("上り", "鹿児島駅前 方面"),
                ("下り", "郡元 方面"),
            ]
        else:
            return [
                ("上り", "鹿児島駅前 方面"),
                ("下り", "谷山／郡元 方面"),
            ]


class TramPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.data_manager = TimetableDataManager()

        self.stop_input = ft.Dropdown(
            label="停留所を選択",
            options=[ft.dropdown.Option(stop) for stop in self.data_manager.get_stops()],
            bgcolor=WHITE,
            border_radius=8,
            width=300,
            on_change=self._on_stop_change,
        )

        self.direction_input = ft.Dropdown(
            label="方向を選択",
            options=[ft.dropdown.Option(key=k, text=t) for k, t in get_direction_options("鹿児島駅前")],
            bgcolor=WHITE,
            border_radius=8,
            width=300,
            on_change=self._on_selection_change,
        )

        self.result_display = ft.Column(spacing=0, scroll=ft.ScrollMode.AUTO)

        if self.stop_input.options:
            self.stop_input.value = self.data_manager.get_stops()[0]
            options = get_direction_options(self.stop_input.value)
            self.direction_input.value = options[0][0]
            current_time = get_current_time()
            trains = self.data_manager.get_next_trains(
                self.stop_input.value, self.direction_input.value, current_time
            )
            self.result_display.controls = create_train_list(
                trains, current_time, self.stop_input.value, self.direction_input.value
            )

    def _on_stop_change(self, e):
        if self.stop_input.value:
            options = get_direction_options(self.stop_input.value)
            self.direction_input.options = [ft.dropdown.Option(key=k, text=t) for k, t in options]
            self.direction_input.value = options[0][0]
            try:
                self.direction_input.update()
            except Exception:
                pass
            self._update_results()

    def _on_selection_change(self, e):
        if self.stop_input.value and self.direction_input.value:
            self._update_results()

    def _update_results(self, e=None):
        if not self.stop_input.value or not self.direction_input.value:
            self.result_display.controls = [
                ft.Text("停留所と方向を選択してください", color=TEXT_SECONDARY)
            ]
        else:
            current_time = get_current_time()
            trains = self.data_manager.get_next_trains(
                self.stop_input.value, self.direction_input.value, current_time
            )
            self.result_display.controls = create_train_list(
                trains, current_time, self.stop_input.value, self.direction_input.value
            )
        try:
            self.page.update()
        except Exception:
            pass

    def set_stop(self, stop_name: str):
        stop_keys = [o.key for o in self.stop_input.options]
        if stop_name in stop_keys:
            self.stop_input.value = stop_name
            options = get_direction_options(stop_name)
            self.direction_input.options = [ft.dropdown.Option(key=k, text=t) for k, t in options]
            self.direction_input.value = options[0][0]
            if hasattr(self, '_page_cache'):
                del self._page_cache

    def create_page(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Row([
                            ft.Text("時刻表", size=20, weight=ft.FontWeight.BOLD, color=WHITE),
                            ft.Text(get_current_time(), size=13, color=WHITE),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=ft.padding.symmetric(horizontal=20, vertical=14),
                        bgcolor=PRIMARY,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                self.stop_input,
                                ft.Container(height=8),
                                self.direction_input,
                                ft.Container(height=8),
                                ft.Text(
                                    "※特別ダイヤの場合は運行情報ページをご確認ください",
                                    size=11,
                                    color=GREY,
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.all(20),
                        bgcolor=WHITE,
                    ),
                    ft.Divider(height=1, color=BORDER),
                    ft.Container(
                        content=self.result_display,
                        padding=ft.padding.all(15),
                        expand=True,
                        bgcolor=BG,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=BG,
            expand=True,
        )