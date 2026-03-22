"""時刻計算ユーティリティ"""

from datetime import datetime
from typing import Optional


def time_to_minutes(time_str: str) -> int:
    """時刻文字列を分単位に変換"""
    try:
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes
    except:
        return 0


def minutes_to_time(minutes: int) -> str:
    """分単位を時刻文字列に変換"""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def get_current_time() -> str:
    """現在時刻を HH:MM 形式で取得"""
    return datetime.now().strftime("%H:%M")


def calculate_wait_time(current_time: str, train_time: str) -> str:
    """待ち時間を計算して文字列で返す"""
    current_minutes = time_to_minutes(current_time)
    train_minutes = time_to_minutes(train_time)
    wait_minutes = train_minutes - current_minutes

    if wait_minutes <= 0:
        return "まもなく"
    else:
        return f"約{wait_minutes}分後"


def get_day_type(dt: Optional[datetime] = None) -> str:
    """曜日区分を返す（"平日" | "土曜" | "日曜祝日"）。

    祝日判定は簡易化のため未実装で、日曜日を「日曜祝日」とし、
    土曜日は「土曜」、それ以外は「平日」を返す。
    必要であれば祝日ライブラリ導入を検討。
    """
    target = dt or datetime.now()
    weekday = target.weekday()  # 0=Mon ... 6=Sun
    if weekday == 5:
        return "土曜"
    if weekday == 6:
        return "日曜祝日"
    return "平日"
