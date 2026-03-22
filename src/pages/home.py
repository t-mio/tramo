import flet as ft
import sys
import json
from pathlib import Path
from utils.timetable_data import TimetableDataManager
from utils.time_utils import get_current_time, calculate_wait_time

_src_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_src_dir))

from theme import BG, WHITE, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY, PRIMARY_LIGHT, GOLD, BORDER, GREY, LINE1, LINE2

PREFS_PATH = Path(__file__).resolve().parents[1] / "assets" / "prefs.json"

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


def get_direction_label(stop: str, direction: str) -> str:
    options = get_direction_options(stop)
    for key, label in options:
        if key == direction:
            return label
    return direction


def load_prefs():
    try:
        with open(PREFS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "favorite_stop1": "加治屋町",
            "favorite_direction1": "上り",
            "favorite_stop2": "天文館通",
            "favorite_direction2": "下り",
        }


def save_prefs(stop1, direction1, stop2, direction2):
    try:
        with open(PREFS_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "favorite_stop1": stop1,
                "favorite_direction1": direction1,
                "favorite_stop2": stop2,
                "favorite_direction2": direction2,
            }, f, ensure_ascii=False)
    except Exception as e:
        print(f"prefs保存エラー: {e}")


class HomePage:
    def __init__(self, page: ft.Page, app=None):
        self.page = page
        self.app = app
        self.data_manager = TimetableDataManager()

        prefs = load_prefs()
        self.favorite_stop1 = prefs.get("favorite_stop1", "加治屋町")
        self.favorite_direction1 = prefs.get("favorite_direction1", "上り")
        self.favorite_stop2 = prefs.get("favorite_stop2", "天文館通")
        self.favorite_direction2 = prefs.get("favorite_direction2", "下り")

        self.time_text = ft.Text(
            get_current_time(),
            size=54,
            color=WHITE,
            weight=ft.FontWeight.W_800,
        )
        self.stop_text1 = ft.Text(
            f"⭐ {self.favorite_stop1}  {get_direction_label(self.favorite_stop1, self.favorite_direction1)}",
            size=13, color=GOLD, weight=ft.FontWeight.W_600,
        )
        self.stop_text2 = ft.Text(
            f"⭐ {self.favorite_stop2}  {get_direction_label(self.favorite_stop2, self.favorite_direction2)}",
            size=13, color=GOLD, weight=ft.FontWeight.W_600,
        )
        self.train_column1 = ft.Column(spacing=4)
        self.train_column2 = ft.Column(spacing=4)
        self._refresh_trains()

    def _refresh_trains(self):
        for stop, direction, column in [
            (self.favorite_stop1, self.favorite_direction1, self.train_column1),
            (self.favorite_stop2, self.favorite_direction2, self.train_column2),
        ]:
            trains = self.data_manager.get_next_trains(stop, direction, get_current_time())
            rows = []
            for t in trains[:4]:
                wait_str = calculate_wait_time(get_current_time(), t["time"])
                rows.append(
                    ft.Row([
                        ft.Container(
                            content=ft.Text(t["line"], color=WHITE, size=11, weight=ft.FontWeight.BOLD),
                            width=24, height=24,
                            bgcolor=LINE1 if t["line"] == "1" else LINE2,
                            border_radius=4,
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(t["time"], size=14, weight=ft.FontWeight.BOLD, color=WHITE),
                        ft.Text(wait_str, size=11, color=GOLD),
                    ], spacing=6)
                )
            column.controls = rows

    def _show_stop_picker(self, e):
        if self.app:
            self.app.pause_update()

        stops = self.data_manager.get_stops()

        # 方向ドロップダウンを停留所に連動して更新する
        def make_dir_dropdown(stop_val, dir_val):
            opts = get_direction_options(stop_val)
            return ft.Dropdown(
                options=[ft.dropdown.Option(key=k, text=t) for k, t in opts],
                value=dir_val if any(k == dir_val for k, _ in opts) else opts[0][0],
                width=240,
            )

        dir1_ref = [make_dir_dropdown(self.favorite_stop1, self.favorite_direction1)]
        dir2_ref = [make_dir_dropdown(self.favorite_stop2, self.favorite_direction2)]

        dir1_container = ft.Container(content=dir1_ref[0])
        dir2_container = ft.Container(content=dir2_ref[0])

        stop1 = ft.Dropdown(
            label="停留所①",
            options=[ft.dropdown.Option(s) for s in stops],
            value=self.favorite_stop1,
            width=240,
        )
        stop2 = ft.Dropdown(
            label="停留所②",
            options=[ft.dropdown.Option(s) for s in stops],
            value=self.favorite_stop2,
            width=240,
        )

        def on_stop1_change(e):
            dir1_ref[0] = make_dir_dropdown(stop1.value, "下り")
            dir1_container.content = dir1_ref[0]
            try:
                dir1_container.update()
            except Exception:
                pass

        def on_stop2_change(e):
            dir2_ref[0] = make_dir_dropdown(stop2.value, "下り")
            dir2_container.content = dir2_ref[0]
            try:
                dir2_container.update()
            except Exception:
                pass

        stop1.on_change = on_stop1_change
        stop2.on_change = on_stop2_change

        def save(e):
            self.favorite_stop1 = stop1.value
            self.favorite_direction1 = dir1_ref[0].value
            self.favorite_stop2 = stop2.value
            self.favorite_direction2 = dir2_ref[0].value
            save_prefs(self.favorite_stop1, self.favorite_direction1, self.favorite_stop2, self.favorite_direction2)
            self.stop_text1.value = f"⭐ {self.favorite_stop1}  {get_direction_label(self.favorite_stop1, self.favorite_direction1)}"
            self.stop_text2.value = f"⭐ {self.favorite_stop2}  {get_direction_label(self.favorite_stop2, self.favorite_direction2)}"
            self._refresh_trains()
            self.page.close(dlg)
            try:
                self.page.update()
            except Exception:
                pass
            if self.app:
                self.app.resume_update()

        def cancel(e):
            self.page.close(dlg)
            if self.app:
                self.app.resume_update()

        dlg = ft.AlertDialog(
            title=ft.Text("お気に入り停留所の設定"),
            content=ft.Column([
                stop1,
                dir1_container,
                ft.Divider(),
                stop2,
                dir2_container,
            ], spacing=8, tight=True, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("キャンセル", on_click=cancel),
                ft.ElevatedButton("保存", on_click=save),
            ],
        )
        self.page.open(dlg)

    def create_page(self):
        background = ft.Image(
            src="kiriko nakami.jpeg",
            width=float("inf"),
            height=float("inf"),
            fit=ft.ImageFit.COVER,
        )

        card = ft.Container(
            content=ft.Card(
                color="#AA000000",
                content=ft.Container(
                    content=ft.Column(
                        [
                            self.time_text,
                            self.stop_text1,
                            self.train_column1,
                            ft.Divider(color="#44FFFFFF", height=1),
                            self.stop_text2,
                            self.train_column2,
                            ft.TextButton(
                                "停留所を変更",
                                on_click=self._show_stop_picker,
                                style=ft.ButtonStyle(color=GOLD),
                            ),
                        ],
                        spacing=6,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.all(20),
                    width=310,
                ),
            ),
        )

        return ft.Stack(
            [background, card],
            alignment=ft.alignment.center,
            expand=True,
        )