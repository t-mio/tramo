import flet as ft
from typing import Dict, Any, List
from pathlib import Path
import sys

_src_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_src_dir))

from theme import BG, WHITE, TEXT_PRIMARY, TEXT_SECONDARY, PRIMARY, PRIMARY_LIGHT, GOLD, BORDER, GREY, LINE1, LINE2
from utils.time_utils import calculate_wait_time


def create_train_card(train: Dict[str, Any], current_time: str) -> ft.Container:
    wait_text = calculate_wait_time(current_time, train["time"])
    is_line1 = train["line"] == "1"

    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text(
                    train["line"],
                    color=WHITE,
                    size=13,
                    weight=ft.FontWeight.BOLD,
                ),
                width=32,
                height=32,
                bgcolor=LINE1 if is_line1 else LINE2,
                border_radius=6,
                alignment=ft.alignment.center,
            ),
            ft.Column([
                ft.Text(train["time"], size=20, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
                ft.Text(train["line_name"], size=11, color=TEXT_SECONDARY),
            ], spacing=1, expand=True),
            ft.Text(wait_text, size=13, color=PRIMARY, weight=ft.FontWeight.W_600),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.symmetric(horizontal=15, vertical=12),
        bgcolor=WHITE,
        border=ft.border.all(1, BORDER),
        border_radius=10,
        margin=ft.margin.only(bottom=8),
    )


def create_search_header(current_time: str, stop: str, direction: str) -> ft.Container:
    return ft.Container(
        content=ft.Row([
            ft.Text(f"{stop}（{direction}）", size=15, weight=ft.FontWeight.BOLD, color=TEXT_PRIMARY),
            ft.Text(f"現在 {current_time}", size=13, color=TEXT_SECONDARY),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=15, vertical=10),
        bgcolor=PRIMARY_LIGHT,
        border_radius=8,
        margin=ft.margin.only(bottom=10),
    )


def create_train_list(trains: List[Dict[str, Any]], current_time: str,
                      stop: str, direction: str) -> List[ft.Control]:
    if not trains:
        return [
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.NIGHTLIGHT_ROUND, size=40, color=GREY),
                    ft.Text(
                        "本日の運行は終了しました",
                        size=15,
                        color=TEXT_SECONDARY,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Text(
                        "明日の始発は6:00頃です",
                        size=12,
                        color=GREY,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8),
                padding=ft.padding.all(30),
                alignment=ft.alignment.center,
            )
        ]
    controls = [create_search_header(current_time, stop, direction)]
    controls.extend([create_train_card(train, current_time) for train in trains])
    return controls