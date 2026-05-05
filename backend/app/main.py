from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from .database import Base, engine, SessionLocal
from .models import Fish, SensorRecord, Alert
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


@app.get("/")
def root():
    return {"message": "Smart Cold Chain API is running"}


@app.post("/sensor-data")
def create_sensor_data(data: SensorDataCreate, db: Session = Depends(get_db)):
    status = check_status(data.temperature)

    fish = db.query(Fish).filter(Fish.fish_id == data.fish_id).first()

    if not fish:
        fish = Fish(
            fish_id=data.fish_id,
            species=data.species,
            warehouse_id=data.warehouse_id,
            status=status,
            latest_temperature=data.temperature,
            latest_humidity=data.humidity,
            updated_at=datetime.utcnow()
        )
        db.add(fish)
    else:
        now = datetime.utcnow()

        if status != "normal" and fish.updated_at:
            delta = int((now - fish.updated_at).total_seconds())
            delta = max(0, min(delta, 300))  # 避免暴增
            fish.cumulative_over_temp_seconds += delta
        fish.species = data.species
        fish.warehouse_id = data.warehouse_id
        fish.status = status
        fish.latest_temperature = data.temperature
        fish.latest_humidity = data.humidity
        fish.updated_at = datetime.utcnow()

    record = SensorRecord(
        fish_id=data.fish_id,
        temperature=data.temperature,
        humidity=data.humidity,
        timestamp=datetime.utcnow()
    )
    db.add(record)

    if status != "normal":
        level = "嚴重異常" if status == "danger" else "警告"
        message = f"{data.fish_id} 溫度異常，目前溫度 {data.temperature}°C"

        alert = Alert(
            fish_id=data.fish_id,
            level=level,
            message=message,
            temperature=data.temperature,
            timestamp=datetime.utcnow()
        )
        db.add(alert)

    db.commit()

    return {
        "message": "sensor data saved",
        "fish_id": data.fish_id,
        "status": status
    }


@app.get("/fish")
def get_fish_list(db: Session = Depends(get_db)):
    fish_list = db.query(Fish).all()
    return fish_list


@app.get("/fish/{fish_id}")
def get_fish_detail(fish_id: str, db: Session = Depends(get_db)):
    fish = db.query(Fish).filter(Fish.fish_id == fish_id).first()

    records = (
        db.query(SensorRecord)
        .filter(SensorRecord.fish_id == fish_id)
        .order_by(SensorRecord.timestamp.desc())
        .limit(30)
        .all()
    )

    alerts = (
        db.query(Alert)
        .filter(Alert.fish_id == fish_id)
        .order_by(Alert.timestamp.desc())
        .limit(10)
        .all()
    )

    return {
        "fish": fish,
        "records": list(reversed(records)),
        "alerts": alerts
    }


@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(50).all()
    return alerts


@app.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    fish_list = db.query(Fish).all()
    alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(10).all()

    total = len(fish_list)
    abnormal = len([f for f in fish_list if f.status != "normal"])

    temps = [
        f.latest_temperature
        for f in fish_list
        if f.latest_temperature is not None
    ]

    avg_temp = round(sum(temps) / len(temps), 2) if temps else None

    return {
        "total_fish": total,
        "normal_count": total - abnormal,
        "abnormal_count": abnormal,
        "average_temperature": avg_temp,
        "latest_alerts": alerts
    }