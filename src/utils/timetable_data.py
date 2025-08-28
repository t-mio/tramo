"""時刻表データ処理クラス"""
import json
from typing import List, Dict, Any
from .time_utils import time_to_minutes


class TimetableDataManager:
    """時刻表データの管理と検索"""
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict[str, Any]:
        """サンプル時刻表データの読み込み"""
        try:
            with open("./src/assets/sample_timetable.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print("サンプル時刻表データが見つかりません")
            return {}
        except Exception as e:
            print(f"データ読み込みエラー: {e}")
            return {}
    
    def get_stops(self) -> List[str]:
        """停留所一覧を取得"""
        if self.data and "stops" in self.data:
            return list(self.data["stops"].keys())
        return []
    
    def get_next_trains(self, stop: str, direction: str, current_time: str) -> List[Dict[str, Any]]:
        """次の5件の市電を取得"""
        if not self.data or "stops" not in self.data:
            return []
        
        if stop not in self.data["stops"]:
            return []
        
        stop_data = self.data["stops"][stop]
        if "directions" not in stop_data or direction not in stop_data["directions"]:
            return []
        
        direction_data = stop_data["directions"][direction]
        current_minutes = time_to_minutes(current_time)
        all_trains = []
        
        # 1系統と2系統の時刻を統合
        for line_id in ["1", "2"]:
            if line_id in direction_data:
                line_info = self.data["lines"][line_id]
                for time_str in direction_data[line_id]:
                    train_minutes = time_to_minutes(time_str)
                    if train_minutes >= current_minutes:
                        all_trains.append({
                            "time": time_str,
                            "line": line_id,
                            "line_name": line_info["name"],
                            "color": line_info["color_code"],
                            "minutes": train_minutes
                        })
        
        # 時刻順でソートして上位5件を返す
        all_trains.sort(key=lambda x: x["minutes"])
        return all_trains[:5]
