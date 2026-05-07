from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from datetime import datetime

from .database import Base, engine, SessionLocal
from .models import FishBox, SensorRecord, Alert
from .schemas import SensorDataCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Cold Chain API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_status(temperature: float):

    if temperature > -15:
        return "danger"

    elif temperature > -18:
        return "warning"

    else:
        return "normal"


def calculate_current_grade(initial_grade: str, status: str):

    grade_order = ["A", "B", "C"]

    initial_grade = initial_grade.upper()

    if initial_grade not in grade_order:
        initial_grade = "B"

    index = grade_order.index(initial_grade)

    if status == "warning":
        index += 1

    elif status == "danger":
        index += 2

    if index >= len(grade_order):
        index = len(grade_order) - 1

    return grade_order[index]


def calculate_estimated_price(
    species: str,
    weight: float,
    current_grade: str
):

    base_prices = {
        "Tuna": 180,
        "Salmon": 150,
        "Mackerel": 90,
        "Cod": 120,
        "鮪魚": 180,
        "鮭魚": 150,
        "鯖魚": 90,
        "鱈魚": 120,
    }

    grade_factor = {
        "A": 1.2,
        "B": 1.0,
        "C": 0.7,
    }

    base_price = base_prices.get(species, 100)

    factor = grade_factor.get(current_grade, 1.0)

    return round(base_price * weight * factor, 0)


@app.get("/")
def root():
    return {"message": "Smart Cold Chain API is running"}


@app.post("/sensor-data")
def create_sensor_data(
    data: SensorDataCreate,
    db: Session = Depends(get_db)
):

    status = check_status(data.temperature)

    current_grade = calculate_current_grade(
        data.initial_grade,
        status
    )

    estimated_price = calculate_estimated_price(
        data.species,
        data.weight,
        current_grade
    )

    fish_box = db.query(FishBox).filter(
        FishBox.box_id == data.box_id
    ).first()

    if not fish_box:

        fish_box = FishBox(
            box_id=data.box_id,

            species=data.species,

            weight=data.weight,
            quantity=data.quantity,

            initial_grade=data.initial_grade.upper(),
            current_grade=current_grade,

            warehouse_id=data.warehouse_id,

            status=status,

            latest_temperature=data.temperature,
            latest_humidity=data.humidity,

            estimated_price=estimated_price,

            updated_at=datetime.utcnow()
        )

        db.add(fish_box)

    else:

        fish_box.species = data.species

        fish_box.weight = data.weight
        fish_box.quantity = data.quantity

        fish_box.initial_grade = data.initial_grade.upper()

        fish_box.current_grade = current_grade

        fish_box.warehouse_id = data.warehouse_id

        fish_box.status = status

        fish_box.latest_temperature = data.temperature
        fish_box.latest_humidity = data.humidity

        fish_box.estimated_price = estimated_price

        fish_box.updated_at = datetime.utcnow()

    record = SensorRecord(
        box_id=data.box_id,

        temperature=data.temperature,
        humidity=data.humidity,

        timestamp=datetime.utcnow()
    )

    db.add(record)

    if status != "normal":

        level = "嚴重異常" if status == "danger" else "警告"

        message = (
            f"{data.box_id} 溫度異常，"
            f"目前溫度 {data.temperature}°C，"
            f"目前分級降為 {current_grade} 級"
        )

        alert = Alert(
            box_id=data.box_id,

            level=level,

            message=message,

            temperature=data.temperature,

            timestamp=datetime.utcnow()
        )

        db.add(alert)

    db.commit()

    return {
        "message": "sensor data saved",

        "box_id": data.box_id,

        "status": status,

        "initial_grade": data.initial_grade,

        "current_grade": current_grade,

        "estimated_price": estimated_price
    }


@app.get("/boxes")
def get_box_list(db: Session = Depends(get_db)):

    box_list = db.query(FishBox).all()

    return box_list


@app.get("/boxes/{box_id}")
def get_box_detail(
    box_id: str,
    db: Session = Depends(get_db)
):

    fish_box = db.query(FishBox).filter(
        FishBox.box_id == box_id
    ).first()

    records = (
        db.query(SensorRecord)
        .filter(SensorRecord.box_id == box_id)
        .order_by(SensorRecord.timestamp.desc())
        .limit(30)
        .all()
    )

    alerts = (
        db.query(Alert)
        .filter(Alert.box_id == box_id)
        .order_by(Alert.timestamp.desc())
        .limit(10)
        .all()
    )

    return {
        "box": fish_box,

        "records": list(reversed(records)),

        "alerts": alerts
    }


@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):

    alerts = (
        db.query(Alert)
        .order_by(Alert.timestamp.desc())
        .limit(50)
        .all()
    )

    return alerts


@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):

    box_list = db.query(FishBox).all()

    alerts = (
        db.query(Alert)
        .order_by(Alert.timestamp.desc())
        .limit(10)
        .all()
    )

    total = len(box_list)

    abnormal = len([
        b for b in box_list
        if b.status != "normal"
    ])

    temps = [
        b.latest_temperature
        for b in box_list
        if b.latest_temperature is not None
    ]

    total_value = sum([
        b.estimated_price
        for b in box_list
        if b.estimated_price is not None
    ])

    avg_temp = (
        round(sum(temps) / len(temps), 2)
        if temps else None
    )

    return {
        "total_boxes": total,

        "normal_count": total - abnormal,

        "abnormal_count": abnormal,

        "average_temperature": avg_temp,

        "total_estimated_value": total_value,

        "latest_alerts": alerts
    }