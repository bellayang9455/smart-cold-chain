import requests
import random
import time

API_URL = "https://smart-cold-api.onrender.com/sensor-data"

box_list = [
    {
        "box_id": "BOX001",
        "species": "Tuna",
        "weight": 42,
        "quantity": 5,
        "initial_grade": "A",
        "warehouse_id": "A01"
    },
    {
        "box_id": "BOX002",
        "species": "Salmon",
        "weight": 35,
        "quantity": 8,
        "initial_grade": "A",
        "warehouse_id": "A01"
    },
    {
        "box_id": "BOX003",
        "species": "Mackerel",
        "weight": 28,
        "quantity": 20,
        "initial_grade": "B",
        "warehouse_id": "A02"
    },
    {
        "box_id": "BOX004",
        "species": "Cod",
        "weight": 31,
        "quantity": 12,
        "initial_grade": "B",
        "warehouse_id": "A02"
    },
    {
        "box_id": "BOX005",
        "species": "Tuna",
        "weight": 55,
        "quantity": 6,
        "initial_grade": "A",
        "warehouse_id": "A03"
    },
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

    box = random.choice(box_list)

    payload = {
        "box_id": box["box_id"],

        "species": box["species"],

        "weight": box["weight"],

        "quantity": box["quantity"],

        "initial_grade": box["initial_grade"],

        "warehouse_id": box["warehouse_id"],

        "temperature": generate_temperature(),

        "humidity": round(random.uniform(60, 75), 1)
    }

    try:

        print("送出資料：", payload)

        response = requests.post(
            API_URL,
            json=payload
        )

        print("狀態碼：", response.status_code)

        print("回應內容：", response.text)

    except Exception as e:

        print("送資料失敗：", e)

    time.sleep(3)