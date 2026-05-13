"""
Telemetry Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TelemetryBase(BaseModel):
    """Base telemetry schema"""
    vehicle_id: str = Field(..., min_length=1, max_length=36)
    latitude: Decimal = Field(..., ge=-90, le=90, decimal_places=8)
    longitude: Decimal = Field(..., ge=-180, le=180, decimal_places=8)
    speed: Optional[Decimal] = Field(None, ge=0, le=999.99)
    battery_level: Optional[Decimal] = Field(None, ge=0, le=100)
    heading: Optional[Decimal] = Field(None, ge=0, le=360)
    odometer: Optional[Decimal] = Field(None, ge=0)


class TelemetryCreate(TelemetryBase):
    """Schema for creating telemetry data"""
    pass


class TelemetryResponse(TelemetryBase):
    """Schema for telemetry response"""
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Made with Bob
