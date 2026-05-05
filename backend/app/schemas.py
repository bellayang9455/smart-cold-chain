from pydantic import BaseModel
from datetime import datetime


class SensorDataCreate(BaseModel):
    fish_id: str
    species: str
    warehouse_id: str
    temperature: float
    humidity: float


class FishResponse(BaseModel):
    fish_id: str
    species: str
    warehouse_id: str
    status: str
    latest_temperature: float | None
    latest_humidity: float | None
    updated_at: datetime | None

    class Config:
        from_attributes = True