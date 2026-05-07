from pydantic import BaseModel
from datetime import datetime


class SensorDataCreate(BaseModel):
    box_id: str

    species: str

    weight: float
    quantity: int

    initial_grade: str

    warehouse_id: str

    temperature: float
    humidity: float


class BoxResponse(BaseModel):
    box_id: str

    species: str

    weight: float
    quantity: int

    initial_grade: str
    current_grade: str

    warehouse_id: str

    status: str

    latest_temperature: float | None
    latest_humidity: float | None

    estimated_price: float | None

    updated_at: datetime | None

    class Config:
        from_attributes = True