import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from .time_utils import time_to_minutes


class TimetableDataManager:
    def __init__(self):
        self.data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        try:
            path = Path(__file__).resolve().parents[1] / "assets" / "sample_timetable.json"
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("サンプル時刻表データが見つかりません")
            return {}
        except Exception as e:
            print(f"データ読み込みエラー: {e}")
            return {}

    def _get_day_type(self) -> str:
        today = datetime.now()
        weekday = today.weekday()
        try:
            import jpholiday
            is_holiday = jpholiday.is_holiday(today)
        except ImportError:
            is_holiday = False
        if weekday == 6 or is_holiday:
            return "日曜祝日"
        elif weekday == 5:
            return "土曜"
        else:
            return "平日"

    def get_stops(self) -> List[str]:
        if self.data and "stops" in self.data:
            return list(self.data["stops"].keys())
        return []

    def get_next_trains(self, stop: str, direction: str, current_time: str) -> List[Dict[str, Any]]:
        if not self.data or "stops" not in self.data:
            return []
        if stop not in self.data["stops"]:
            return []

        stop_data = self.data["stops"][stop]
        if "directions" not in stop_data or direction not in stop_data["directions"]:
            return []

        direction_data = stop_data["directions"][direction]
        day_type = self._get_day_type()

        if day_type not in direction_data:
            day_type = list(direction_data.keys())[0]

        day_data = direction_data[day_type]
        current_minutes = time_to_minutes(current_time)
        all_trains = []

        for line_id in ["1", "2"]:
            if line_id in day_data:
                line_info = self.data["lines"][line_id]
                for time_str in day_data[line_id]:
                    train_minutes = time_to_minutes(time_str)
                    if train_minutes >= current_minutes:
                        all_trains.append({
                            "time": time_str,
                            "line": line_id,
                            "line_name": line_info["name"],
                            "color": line_info["color_code"],
                            "minutes": train_minutes
                        })

        all_trains.sort(key=lambda x: x["minutes"])
        return all_trains[:5]

    def is_service_ended(self, stop: str, direction: str, current_time: str) -> bool:
        """本日の運行が終了しているか確認"""
        if not self.data or "stops" not in self.data:
            return False
        if stop not in self.data["stops"]:
            return False

        stop_data = self.data["stops"][stop]
        if "directions" not in stop_data or direction not in stop_data["directions"]:
            return False

        direction_data = stop_data["directions"][direction]
        day_type = self._get_day_type()
        if day_type not in direction_data:
            day_type = list(direction_data.keys())[0]

        day_data = direction_data[day_type]
        current_minutes = time_to_minutes(current_time)

        for line_id in ["1", "2"]:
            if line_id in day_data:
                last_time = day_data[line_id][-1]
                if time_to_minutes(last_time) >= current_minutes:
                    return False
        return True