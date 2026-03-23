import flet as ft
import threading
from data.tram_data import get_tram_data
from pages.home import HomePage
from pages.map import MapPage
from pages.tram import TramPage
from pages.schedule import SchedulePage
from pages.payment import PaymentPage
from components.bottom_nav import BottomNavigation
from utils.time_utils import get_current_time


class MobileApp:
    def __init__(self):
        self.current_page_index = 0
        self.pages = []
        self.main_content = None
        self.bottom_nav = None
        self._running = False
        self._page = None
        self._lock = threading.Lock()
        self._paused = False
        self._map_updating = False

    def pause_update(self):
        self._paused = True

    def resume_update(self):
        self._paused = False

    def main(self, page: ft.Page):
        get_tram_data()
        page.title = "Tramo"
        page.window.width = 390
        page.window.height = 844
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.bgcolor = ft.Colors.GREY_100
        page.theme_mode = ft.ThemeMode.LIGHT

        self.pages = [
            HomePage(page, self),
            MapPage(page, self),
            TramPage(page),
            SchedulePage(page),
            PaymentPage(page),
        ]

        first_page = self.pages[0].create_page()
        self.pages[0]._page_cache = first_page

        self.main_content = ft.Container(
            content=first_page,
            expand=True,
            bgcolor=ft.Colors.WHITE,
        )

        self.bottom_nav = BottomNavigation(page, self.on_nav_change)
        nav_bar = self.bottom_nav.create_bottom_nav()
        self._nav_bar = nav_bar

        page.add(
            ft.Column(
                [self.main_content, nav_bar],
                spacing=0,
                expand=True,
            )
        )
        page.update()

        self._running = True
        self._page = page

        def on_disconnect(e):
            self._running = False
        page.on_disconnect = on_disconnect

        self._start_timer()

    def _start_timer(self):
        def tick():
            while self._running:
                index = self.current_page_index

                if index == 1:
                    threading.Event().wait(5.0)
                else:
                    if index == 0:
                        wait = 3.0
                    elif index == 2:
                        wait = 30.0
                    else:
                        wait = 60.0
                    threading.Event().wait(wait)

                if not self._running or self._paused:
                    continue
                if self._lock.locked():
                    continue
                try:
                    self._auto_update()
                except Exception:
                    pass

        t = threading.Thread(target=tick, daemon=True)
        t.start()

    def _auto_update(self):
        index = self.current_page_index

        if index == 0:
            with self._lock:
                home = self.pages[0]
                if hasattr(home, 'time_text'):
                    home.time_text.value = get_current_time()
                    try:
                        home.time_text.update()
                    except Exception:
                        pass

        elif index == 1:
            if self._map_updating:
                return
            self._map_updating = True
            try:
                map_page = self.pages[1]
                if hasattr(map_page, '_update_train_positions'):
                    map_page._update_train_positions()
            except Exception:
                pass
            finally:
                self._map_updating = False

        elif index == 2:
            with self._lock:
                tram = self.pages[2]
                if hasattr(tram, '_update_results'):
                    try:
                        tram._update_results()
                    except Exception:
                        pass

    def on_nav_change(self, index: int):
        with self._lock:
            self.current_page_index = index
            if 0 <= index < len(self.pages):
                if not hasattr(self.pages[index], '_page_cache'):
                    self.pages[index]._page_cache = self.pages[index].create_page()
                self.main_content.content = self.pages[index]._page_cache
                self.main_content.update()


def main():
    ft.app(target=lambda page: MobileApp().main(page), view=ft.AppView.WEB_BROWSER)


main()
