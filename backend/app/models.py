from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class Fish(Base):
    __tablename__ = "fish"

    id = Column(Integer, primary_key=True, index=True)
    fish_id = Column(String, unique=True, index=True)
    species = Column(String)
    warehouse_id = Column(String)
    status = Column(String, default="normal")
    latest_temperature = Column(Float, nullable=True)
    latest_humidity = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    cumulative_over_temp_seconds = Column(Integer, default=0)


class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id = Column(Integer, primary_key=True, index=True)
    fish_id = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    fish_id = Column(String, index=True)
    level = Column(String)
    message = Column(String)
    temperature = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)