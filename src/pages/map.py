import flet as ft
import flet_map as ftm
import json
import math
from pathlib import Path
from utils.train_position import get_train_positions

LINE1_STOPS = [
    "鹿児島駅前", "桜島桟橋通", "水族館口", "市役所前", "朝日通",
    "いづろ通", "天文館通", "高見馬場", "甲東中学校前", "新屋敷",
    "武之橋", "二中通（キラメキテラス前）", "荒田八幡", "騎射場",
    "鴨池", "郡元", "涙橋", "南鹿児島駅前", "二軒茶屋",
    "宇宿一丁目", "脇田", "笹貫", "上塩屋", "谷山"
]

LINE2_STOPS = [
    "鹿児島駅前", "桜島桟橋通", "水族館口", "市役所前", "朝日通",
    "いづろ通", "天文館通", "高見馬場", "加治屋町", "高見橋",
    "鹿児島中央駅前", "都通", "中洲通", "市立病院前", "神田（交通局前）",
    "唐湊", "工学部前", "純心学園前", "中郡", "郡元"
]


class MapPage:
    def __init__(self, page: ft.Page, app=None):
        self.page = page
        self.app = app
        self.stops = self._load_stops()
        self.stops_coords = {s["name"]: {"lat": s["lat"], "lng": s["lng"]} for s in self.stops}
        self.current_lat = None
        self.current_lng = None
        self.nearest_stop = None
        self.selected_line = None
        self.selected_dest = None
        self.polyline_layer = self._create_polyline_layer()
        self.marker_layer = ftm.MarkerLayer(markers=self._create_stop_markers())
        self.current_marker_layer = ftm.MarkerLayer(markers=[])
        self.train_marker_layer = ftm.MarkerLayer(markers=[])
        self.nearest_card = ft.Container(visible=False)
        self.status_text = ft.Text("", size=13, color=ft.Colors.GREY_600)

        self.btn_line1 = ft.ElevatedButton(
            "1系統", bgcolor=ft.Colors.GREY_400, color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
            on_click=lambda e: self._select_line("1"),
        )
        self.btn_line2 = ft.ElevatedButton(
            "2系統", bgcolor=ft.Colors.GREY_400, color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
            on_click=lambda e: self._select_line("2"),
        )
        self.btn_taiyama = ft.ElevatedButton(
            "谷山", bgcolor=ft.Colors.GREY_400, color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
            on_click=lambda e: self._select_dest("谷山"),
        )
        self.btn_koriyama = ft.ElevatedButton(
            "郡元", bgcolor=ft.Colors.GREY_400, color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
            on_click=lambda e: self._select_dest("郡元"),
        )
        self.btn_kagoshima = ft.ElevatedButton(
            "鹿児島駅前", bgcolor=ft.Colors.GREY_400, color=ft.Colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=6)),
            on_click=lambda e: self._select_dest("鹿児島駅前"),
        )

        self.geo = ft.Geolocator(on_position_change=self._on_position)
        self.page.overlay.append(self.geo)

    def _select_line(self, line):
        self.selected_line = None if self.selected_line == line else line
        self._update_buttons()
        self._refresh_markers()

    def _select_dest(self, dest):
        self.selected_dest = None if self.selected_dest == dest else dest
        self._update_buttons()
        self._refresh_markers()

    def _update_buttons(self):
        self.btn_line1.bgcolor = ft.Colors.BLUE if self.selected_line == "1" else ft.Colors.GREY_400
        self.btn_line2.bgcolor = ft.Colors.RED if self.selected_line == "2" else ft.Colors.GREY_400
        self.btn_taiyama.bgcolor = ft.Colors.BLUE_700 if self.selected_dest == "谷山" else ft.Colors.GREY_400
        self.btn_koriyama.bgcolor = ft.Colors.RED_700 if self.selected_dest == "郡元" else ft.Colors.GREY_400
        self.btn_kagoshima.bgcolor = ft.Colors.GREEN_700 if self.selected_dest == "鹿児島駅前" else ft.Colors.GREY_400
        try:
            self.btn_line1.update()
            self.btn_line2.update()
            self.btn_taiyama.update()
            self.btn_koriyama.update()
            self.btn_kagoshima.update()
        except Exception:
            pass

    def _refresh_markers(self, e=None):
        filtered_stops = self.stops
        if self.selected_line is not None:
            line_num = int(self.selected_line)
            filtered_stops = [s for s in filtered_stops if line_num in s["lines"]]

        self.marker_layer.markers = [
            ftm.Marker(
                content=ft.GestureDetector(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Text(stop["name"], size=9, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                            bgcolor=ft.Colors.WHITE, padding=ft.padding.symmetric(horizontal=3, vertical=1),
                            border_radius=3, border=ft.border.all(0.5, ft.Colors.GREY_400)),
                        self._make_stop_square(stop["lines"]),
                    ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    on_tap=lambda e, s=stop["name"]: self._on_stop_tap(s),
                ),
                coordinates=ftm.MapLatitudeLongitude(stop["lat"], stop["lng"]),
            )
            for stop in filtered_stops
        ]
        self._update_train_positions()
        try:
            self.page.update()
        except Exception:
            pass

    def _load_stops(self):
        path = Path(__file__).resolve().parents[1] / "assets" / "stops.json"
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)["stops"]
        except Exception as e:
            print(f"stops.json読み込みエラー: {e}")
            return []

    def _create_polyline_layer(self):
        railway_path = Path(__file__).resolve().parents[1] / "assets" / "railway.json"
        try:
            with open(railway_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"railway.json読み込みエラー: {e}")
            return self._create_polyline_layer_fallback()
        polylines = []
        for element in data.get("elements", []):
            if element.get("type") != "way":
                continue
            geometry = element.get("geometry", [])
            if len(geometry) < 2:
                continue
            tags = element.get("tags", {})
            if tags.get("service", "") in ["spur", "siding", "crossover"]:
                continue
            name = tags.get("KSJ2:LIN", "")
            color = "#AAF44336" if ("第二期線" in name or "唐湊線" in name) else "#AA2196F3"
            coords = [ftm.MapLatitudeLongitude(p["lat"], p["lon"]) for p in geometry]
            polylines.append(ftm.PolylineMarker(coordinates=coords, color=color, stroke_width=5))
        return ftm.PolylineLayer(polylines=polylines)

    def _create_polyline_layer_fallback(self):
        line1_coords = [ftm.MapLatitudeLongitude(self.stops_coords[s]["lat"], self.stops_coords[s]["lng"]) for s in LINE1_STOPS if s in self.stops_coords]
        line2_coords = [ftm.MapLatitudeLongitude(self.stops_coords[s]["lat"], self.stops_coords[s]["lng"]) for s in LINE2_STOPS if s in self.stops_coords]
        return ftm.PolylineLayer(polylines=[
            ftm.PolylineMarker(coordinates=line1_coords, color="#AA2196F3", stroke_width=5),
            ftm.PolylineMarker(coordinates=line2_coords, color="#AAF44336", stroke_width=5),
        ])

    def _make_stop_square(self, lines):
        is_line1, is_line2 = 1 in lines, 2 in lines
        shadow = ft.BoxShadow(spread_radius=0, blur_radius=3, color=ft.Colors.BLACK38, offset=ft.Offset(0, 1))
        if is_line1 and is_line2:
            return ft.Container(
                content=ft.Row([ft.Container(width=5, height=10, bgcolor=ft.Colors.BLUE), ft.Container(width=5, height=10, bgcolor=ft.Colors.RED)], spacing=0),
                width=10, height=10, border_radius=2, border=ft.border.all(1.5, ft.Colors.WHITE),
                clip_behavior=ft.ClipBehavior.HARD_EDGE, shadow=shadow,
            )
        bgcolor = ft.Colors.BLUE if is_line1 else ft.Colors.RED
        return ft.Container(width=10, height=10, bgcolor=bgcolor, border_radius=2, border=ft.border.all(1.5, ft.Colors.WHITE), shadow=shadow)

    def _create_stop_markers(self):
        return [
            ftm.Marker(
                content=ft.GestureDetector(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Text(stop["name"], size=9, color=ft.Colors.BLACK, weight=ft.FontWeight.W_500),
                            bgcolor=ft.Colors.WHITE, padding=ft.padding.symmetric(horizontal=3, vertical=1),
                            border_radius=3, border=ft.border.all(0.5, ft.Colors.GREY_400)),
                        self._make_stop_square(stop["lines"]),
                    ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    on_tap=lambda e, s=stop["name"]: self._on_stop_tap(s),
                ),
                coordinates=ftm.MapLatitudeLongitude(stop["lat"], stop["lng"]),
            )
            for stop in self.stops
        ]

    def _update_train_positions(self, e=None):
        try:
            trains = get_train_positions(self.stops_coords)
            markers = []
            for train in trains:
                if self.selected_line is not None and train["line"] != self.selected_line:
                    continue
                if self.selected_dest is not None:
                    if self.selected_dest == "谷山" and not (train["line"] == "1" and train["direction"] == "下り"):
                        continue
                    if self.selected_dest == "郡元" and not (train["line"] == "2" and train["direction"] == "下り"):
                        continue
                    if self.selected_dest == "鹿児島駅前" and train["direction"] != "上り":
                        continue
                bg_color = "#1565C0" if train["line"] == "1" else "#C62828"
                markers.append(ftm.Marker(
                    content=ft.Column([
                        ft.Container(
                            content=ft.Text(f"{train['line']}系 {train['terminal']}行き", size=9, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                            bgcolor=bg_color, padding=ft.padding.symmetric(horizontal=4, vertical=2), border_radius=4,
                            shadow=ft.BoxShadow(spread_radius=0, blur_radius=3, color=ft.Colors.BLACK38, offset=ft.Offset(0, 1)),
                        ),
                        ft.Container(width=2, height=10, bgcolor=bg_color),
                        ft.Container(width=14, height=14, bgcolor=bg_color, border_radius=7,
                            border=ft.border.all(2.5, ft.Colors.WHITE),
                            shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.BLACK38, offset=ft.Offset(0, 2))),
                    ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    coordinates=ftm.MapLatitudeLongitude(train["lat"], train["lng"]),
                ))
            self.train_marker_layer.markers = markers
        except Exception as ex:
            print(f"電車位置更新エラー: {ex}")

    def _calc_distance(self, lat1, lng1, lat2, lng2):
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlng/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    def _find_nearest_stop(self, lat, lng):
        nearest, min_dist = None, float("inf")
        for stop in self.stops:
            dist = self._calc_distance(lat, lng, stop["lat"], stop["lng"])
            if dist < min_dist:
                min_dist, nearest = dist, stop
        return nearest, min_dist

    def _on_position(self, e: ft.GeolocatorPositionChangeEvent):
        self.current_lat, self.current_lng = e.latitude, e.longitude
        self.current_marker_layer.markers = [ftm.Marker(
            content=ft.Stack([
                ft.Container(width=32, height=32, bgcolor="#331A73E8", border_radius=16),
                ft.Container(content=ft.Container(width=16, height=16, bgcolor="#1A73E8", border_radius=8,
                    border=ft.border.all(2.5, ft.Colors.WHITE),
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=6, color=ft.Colors.BLACK38, offset=ft.Offset(0, 2))),
                    alignment=ft.alignment.center, width=32, height=32),
            ], width=32, height=32),
            coordinates=ftm.MapLatitudeLongitude(self.current_lat, self.current_lng),
        )]
        nearest, dist = self._find_nearest_stop(self.current_lat, self.current_lng)
        self.nearest_stop = nearest
        dist_str = f"{int(dist)}m" if dist < 1000 else f"{dist/1000:.1f}km"
        self.status_text.value = f"最寄り: {nearest['name']} ({dist_str})"
        lines_str = "・".join([f"{l}系統" for l in nearest["lines"]])
        self.nearest_card.content = ft.Row([
            ft.Icon(ft.Icons.TRAM, color=ft.Colors.BLUE_600),
            ft.Column([
                ft.Text(nearest["name"], size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"{lines_str} / {dist_str}", size=12, color=ft.Colors.GREY_600),
            ], spacing=2, expand=True),
            ft.TextButton("時刻表", on_click=lambda e: self._on_stop_tap(nearest["name"])),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.nearest_card.visible = True
        try:
            self.page.update()
        except Exception:
            pass

    def _get_location(self, e):
        self.status_text.value = "現在地を取得中..."
        try:
            self.status_text.update()
        except Exception:
            pass
        self.geo.get_current_position()

    def _on_stop_tap(self, stop_name):
        dlg = ft.AlertDialog(
            title=ft.Text(stop_name),
            content=ft.Text("この電停の時刻表を見ますか？"),
            actions=[
                ft.TextButton("閉じる", on_click=lambda e: self.page.close(dlg)),
                ft.ElevatedButton("時刻表を見る", on_click=lambda e: self._go_to_timetable(dlg, stop_name)),
            ],
        )
        self.page.open(dlg)

    def _go_to_timetable(self, dlg, stop_name):
        self.page.close(dlg)
        if self.app:
            tram_page = self.app.pages[2]
            if hasattr(tram_page, 'set_stop'):
                tram_page.set_stop(stop_name)
            self.app.on_nav_change(2)
            self.app._nav_bar.selected_index = 2
            try:
                self.app._nav_bar.update()
            except Exception:
                pass

    def create_page(self):
        self.nearest_card = ft.Container(
            content=ft.Text(""), padding=ft.padding.all(12), bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300), border_radius=10, visible=False, margin=ft.margin.all(10),
        )
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("路線図", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            ft.Row([
                                ft.IconButton(icon=ft.Icons.REFRESH, icon_color=ft.Colors.WHITE, on_click=self._refresh_markers),
                                ft.IconButton(icon=ft.Icons.MY_LOCATION, icon_color=ft.Colors.WHITE, on_click=self._get_location),
                            ]),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            ft.Text("系統:", size=11, color=ft.Colors.WHITE70),
                            self.btn_line1,
                            self.btn_line2,
                        ], spacing=6),
                        ft.Row([
                            ft.Text("行先:", size=11, color=ft.Colors.WHITE70),
                            self.btn_taiyama,
                            self.btn_koriyama,
                            self.btn_kagoshima,
                        ], spacing=6),
                    ], spacing=6),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8), bgcolor=ft.Colors.BLUE_600,
                ),
                ft.Container(
                    content=self.status_text,
                    padding=ft.padding.symmetric(horizontal=15, vertical=5), bgcolor=ft.Colors.GREY_100,
                ),
                self.nearest_card,
                ftm.Map(
                    expand=True,
                    initial_center=ftm.MapLatitudeLongitude(31.578, 130.540),
                    initial_zoom=13,
                    interaction_configuration=ftm.MapInteractionConfiguration(flags=ftm.MapInteractiveFlag.ALL),
                    layers=[
                        ftm.TileLayer(url_template="https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png"),
                        self.polyline_layer,
                        self.marker_layer,
                        self.train_marker_layer,
                        self.current_marker_layer,
                    ],
                ),
            ], spacing=0),
            expand=True,
        )
