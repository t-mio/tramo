import flet as ft
from utils.timetable_data import TimetableDataManager
from utils.time_utils import get_current_time
from components.train_card import create_train_list


class TimetablePage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.data_manager = TimetableDataManager()
        
        # UIコンポーネント
        self.stop_input = ft.Dropdown(
            label="停留所を選択",
            options=[ft.dropdown.Option(stop) for stop in self.data_manager.get_stops()],
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=300,
            on_change=self._on_selection_change,
        )
        
        self.direction_input = ft.Dropdown(
            label="方向を選択",
            options=[ft.dropdown.Option("上り"), ft.dropdown.Option("下り")],
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            width=300,
            on_change=self._on_selection_change,
        )
        
        self.search_button = ft.ElevatedButton(
            text="検索",
            on_click=self._update_results,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            width=280,
            height=45,
        )
        
        self.result_display = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        
        # 初期値設定
        if self.stop_input.options:
            self.stop_input.value = self.data_manager.get_stops()[0]
        
    def _on_selection_change(self, e):
        """選択変更時の自動更新"""
        if self.stop_input.value and self.direction_input.value:
            self._update_results()
    
    def _update_results(self, e=None):
        """検索結果の更新"""
        if not self.stop_input.value or not self.direction_input.value:
            self.result_display.controls = [
                ft.Text("停留所と方向を選択してください", color=ft.Colors.GREY_600)
            ]
        else:
            current_time = get_current_time()
            trains = self.data_manager.get_next_trains(
                self.stop_input.value, 
                self.direction_input.value, 
                current_time
            )
            self.result_display.controls = create_train_list(
                trains, current_time, self.stop_input.value, self.direction_input.value
            )
        
        self.page.update()
    
    def create_page(self):
        """ページレイアウトの作成"""
        return ft.Container(
            content=ft.Column([
                # ヘッダー
                ft.Container(
                    content=ft.Text("市電時刻表", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.BLUE_600,
                    alignment=ft.alignment.center,
                ),
                
                # 検索フォーム
                ft.Container(
                    content=ft.Column([
                        self.stop_input,
                        ft.Container(height=10),
                        self.direction_input,
                        ft.Container(height=15),
                        self.search_button,
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(20),
                    bgcolor=ft.Colors.GREY_50,
                ),
                
                # 検索結果
                ft.Container(
                    content=self.result_display,
                    padding=ft.padding.all(20),
                    expand=True,
                )
            ], spacing=0),
            bgcolor=ft.Colors.WHITE,
            expand=True,
        )