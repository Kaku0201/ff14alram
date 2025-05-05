import json
import os

FILE_PATH = "data/channels.json"


def load_channel_settings():
    if not os.path.exists(FILE_PATH):
        return {}
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_channel_settings(data):
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def add_channel(guild_id, channel_id):
    data = load_channel_settings()
    if str(guild_id) not in data:
        data[str(guild_id)] = []
    if channel_id not in data[str(guild_id)]:
        data[str(guild_id)].append(channel_id)
        save_channel_settings(data)
        return True
    return False


def remove_channel(guild_id, channel_id):
    data = load_channel_settings()
    if str(guild_id) in data and channel_id in data[str(guild_id)]:
        data[str(guild_id)].remove(channel_id)
        if not data[str(guild_id)]:
            del data[str(guild_id)]
        save_channel_settings(data)
        return True
    return False
