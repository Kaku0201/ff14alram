import os
import json

CONFIG_FILE = "config.json"

# 초기 config 생성 또는 불러오기
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"guilds": {}}, f, indent=2)

with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

def get_config():
    return config

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
