import requests
import random
import time

API_URL = "http://127.0.0.1:8000/sensor-data"

fish_list = [
    {"fish_id": "F001", "species": "Tuna", "warehouse_id": "A01"},
    {"fish_id": "F002", "species": "Salmon", "warehouse_id": "A01"},
    {"fish_id": "F003", "species": "Mackerel", "warehouse_id": "A02"},
    {"fish_id": "F004", "species": "Tuna", "warehouse_id": "A02"},
    {"fish_id": "F005", "species": "Cod", "warehouse_id": "A03"},
]


def generate_temperature():
    chance = random.random()

    if chance < 0.75:
        return round(random.uniform(-22.5, -19.0), 1)
    elif chance < 0.93:
        return round(random.uniform(-17.9, -15.1), 1)
    else:
        return round(random.uniform(-14.9, -10.0), 1)


while True:
    fish = random.choice(fish_list)

    payload = {
        "fish_id": fish["fish_id"],
        "species": fish["species"],
        "warehouse_id": fish["warehouse_id"],
        "temperature": generate_temperature(),
        "humidity": round(random.uniform(60, 75), 1)
    }

    try:
        response = requests.post(API_URL, json=payload)
        print(payload, response.json())
    except Exception as e:
        print("送資料失敗：", e)

    time.sleep(3)