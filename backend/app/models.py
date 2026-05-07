from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class FishBox(Base):
    __tablename__ = "fish_boxes"

    id = Column(Integer, primary_key=True, index=True)

    box_id = Column(String, unique=True, index=True)   # 魚貨箱號
    species = Column(String)                          # 魚種
    weight = Column(Float)                            # 重量 kg
    quantity = Column(Integer)                        # 數量
    initial_grade = Column(String)                    # 初始分級 A/B/C
    current_grade = Column(String)                    # 目前分級 A/B/C

    warehouse_id = Column(String)
    status = Column(String, default="normal")

    latest_temperature = Column(Float, nullable=True)
    latest_humidity = Column(Float, nullable=True)

    estimated_price = Column(Float, nullable=True)    # 預估價值
    updated_at = Column(DateTime, default=datetime.utcnow)


class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id = Column(Integer, primary_key=True, index=True)
    box_id = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    box_id = Column(String, index=True)
    level = Column(String)
    message = Column(String)
    temperature = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)