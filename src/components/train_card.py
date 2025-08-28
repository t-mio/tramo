"""市電表示カードコンポーネント"""
import flet as ft
from typing import Dict, Any, List
from utils.time_utils import calculate_wait_time


def create_train_card(train: Dict[str, Any], current_time: str) -> ft.Container:
    """市電情報カードを作成"""
    wait_text = calculate_wait_time(current_time, train["time"])
    
    return ft.Container(
        content=ft.Row([
            # 系統表示（色付き円）
            ft.Container(
                content=ft.Text(
                    train["line"],
                    color=ft.Colors.WHITE,
                    size=16,
                    weight=ft.FontWeight.BOLD
                ),
                width=40,
                height=40,
                bgcolor=train["color"],
                border_radius=20,
                alignment=ft.alignment.center
            ),
            # 時刻と系統名
            ft.Column([
                ft.Text(
                    train["time"],
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK87
                ),
                ft.Text(
                    train["line_name"],
                    size=12,
                    color=ft.Colors.GREY_600
                )
            ], spacing=2),
            # 待ち時間
            ft.Text(
                wait_text,
                size=14,
                color=ft.Colors.BLUE_700,
                weight=ft.FontWeight.W_500
            )
        ], 
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.all(15),
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=10,
        margin=ft.margin.only(bottom=8),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=2,
            color=ft.Colors.GREY_400,
            offset=ft.Offset(0, 1)
        )
    )


def create_search_header(current_time: str, stop: str, direction: str) -> ft.Container:
    """検索結果ヘッダーを作成"""
    return ft.Container(
        content=ft.Row([
            ft.Text(f"現在時刻: {current_time}", 
                   size=16, weight=ft.FontWeight.BOLD),
            ft.Text(f"停留所: {stop} ({direction})",
                   size=14, color=ft.Colors.GREY_700)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.all(15),
        bgcolor=ft.Colors.BLUE_50,
        border_radius=10,
        margin=ft.margin.only(bottom=15)
    )


def create_train_list(trains: List[Dict[str, Any]], current_time: str, 
                      stop: str, direction: str) -> List[ft.Control]:
    """市電リスト全体を作成"""
    if not trains:
        return [ft.Text("該当する市電が見つかりません", color=ft.Colors.GREY_600)]
    
    controls = [create_search_header(current_time, stop, direction)]
    controls.extend([create_train_card(train, current_time) for train in trains])
    return controls
