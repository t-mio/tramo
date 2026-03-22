"""電車の擬似位置情報を計算するモジュール"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from utils.time_utils import time_to_minutes


LINE1_STOPS_DOWN = [
    "鹿児島駅前", "桜島桟橋通", "水族館口", "市役所前", "朝日通",
    "いづろ通", "天文館通", "高見馬場", "甲東中学校前", "新屋敷",
    "武之橋", "二中通（キラメキテラス前）", "荒田八幡", "騎射場",
    "鴨池", "郡元", "涙橋", "南鹿児島駅前", "二軒茶屋",
    "宇宿一丁目", "脇田", "笹貫", "上塩屋", "谷山"
]

LINE2_STOPS_DOWN = [
    "鹿児島駅前", "桜島桟橋通", "水族館口", "市役所前", "朝日通",
    "いづろ通", "天文館通", "高見馬場", "加治屋町", "高見橋",
    "鹿児島中央駅前", "都通", "中洲通", "市立病院前", "神田（交通局前）",
    "唐湊", "工学部前", "純心学園前", "中郡", "郡元"
]

LINE1_STOPS_UP = list(reversed(LINE1_STOPS_DOWN))
LINE2_STOPS_UP = list(reversed(LINE2_STOPS_DOWN))

# 終点
TERMINALS = {
    ("1", "下り"): "谷山",
    ("1", "上り"): "鹿児島駅前",
    ("2", "下り"): "郡元",
    ("2", "上り"): "鹿児島駅前",
}


def _load_timetable() -> Dict:
    path = Path(__file__).resolve().parents[1] / "assets" / "sample_timetable.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _get_day_type() -> str:
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


def get_train_positions(stops_coords: Dict[str, Dict]) -> List[Dict[str, Any]]:
    data = _load_timetable()
    if not data:
        return []

    day_type = _get_day_type()
    now = datetime.now()
    current_minutes = now.hour * 60 + now.minute + now.second / 60

    trains = []

    for line_id, line_name, stops_down, stops_up in [
        ("1", "1系統", LINE1_STOPS_DOWN, LINE1_STOPS_UP),
        ("2", "2系統", LINE2_STOPS_DOWN, LINE2_STOPS_UP),
    ]:
        trains += _calc_positions(
            data, line_id, line_name, "下り", stops_down,
            stops_coords, day_type, current_minutes
        )
        trains += _calc_positions(
            data, line_id, line_name, "上り", stops_up,
            stops_coords, day_type, current_minutes
        )

    return trains


def _calc_positions(
    data, line_id, line_name, direction, stops_order,
    stops_coords, day_type, current_minutes
) -> List[Dict]:
    results = []
    first_stop = stops_order[0]
    terminal = TERMINALS.get((line_id, direction), stops_order[-1])

    try:
        times = data["stops"][first_stop]["directions"][direction][day_type][line_id]
    except (KeyError, TypeError):
        return []

    for dep_time in times:
        dep_minutes = time_to_minutes(dep_time)
        position = _find_train_position(
            data, line_id, direction, stops_order,
            stops_coords, day_type, dep_minutes, current_minutes
        )
        if position:
            position["line"] = line_id
            position["line_name"] = line_name
            position["direction"] = direction
            position["departure"] = dep_time
            position["terminal"] = terminal  # 終点を追加
            results.append(position)

    return results


def _find_train_position(
    data, line_id, direction, stops_order,
    stops_coords, day_type, dep_offset, current_minutes
) -> Optional[Dict]:
    stop_times = []
    for stop in stops_order:
        try:
            times = data["stops"][stop]["directions"][direction][day_type][line_id]
            best = min(times, key=lambda t: abs(
                time_to_minutes(t) - dep_offset - (stop_times[-1][1] - stop_times[0][1] if stop_times else 0)
            ))
            stop_times.append((stop, time_to_minutes(best)))
        except (KeyError, TypeError, ValueError):
            continue

    if len(stop_times) < 2:
        return None

    for i in range(len(stop_times) - 1):
        stop_a, time_a = stop_times[i]
        stop_b, time_b = stop_times[i + 1]

        if time_a <= current_minutes <= time_b:
            if time_b == time_a:
                ratio = 0.5
            else:
                ratio = (current_minutes - time_a) / (time_b - time_a)

            if stop_a not in stops_coords or stop_b not in stops_coords:
                continue

            lat_a = stops_coords[stop_a]["lat"]
            lng_a = stops_coords[stop_a]["lng"]
            lat_b = stops_coords[stop_b]["lat"]
            lng_b = stops_coords[stop_b]["lng"]

            lat = lat_a + (lat_b - lat_a) * ratio
            lng = lng_a + (lng_b - lng_a) * ratio

            return {
                "lat": lat,
                "lng": lng,
                "from_stop": stop_a,
                "to_stop": stop_b,
                "ratio": ratio,
            }

    return None