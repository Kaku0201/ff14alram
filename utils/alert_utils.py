import json
import os

FILE_PATH = "data/alerts.json"


def load_alert_settings():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_alert_settings(data):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def set_alert(guild_id: int, alert_type: str, enabled: bool):
    data = load_alert_settings()
    guild_id = str(guild_id)

    if guild_id not in data:
        data[guild_id] = {}

    data[guild_id][alert_type] = enabled
    save_alert_settings(data)


def get_alert_status(guild_id: int, alert_type: str):
    data = load_alert_settings()
    return data.get(str(guild_id), {}).get(alert_type, False)  # 기본값은 OFF
