from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def home():
    return "봇이 작동 중입니다."  # UptimeRobot이 체크할 응답

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
