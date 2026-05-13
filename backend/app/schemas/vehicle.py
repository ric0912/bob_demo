"""
Vehicle Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from app.models.vehicle import VehicleStatus


class VehicleBase(BaseModel):
    """Base vehicle schema"""
    vin: str = Field(..., min_length=17, max_length=17, description="Vehicle Identification Number")
    make: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=2020, le=2030)
    license_plate: Optional[str] = Field(None, max_length=20)
    battery_capacity: Optional[Decimal] = Field(None, ge=0, le=999.99)


class VehicleCreate(VehicleBase):
    """Schema for creating a vehicle"""
    status: VehicleStatus = VehicleStatus.IDLE


class VehicleUpdate(BaseModel):
    """Schema for updating a vehicle"""
    make: Optional[str] = Field(None, min_length=1, max_length=50)
    model: Optional[str] = Field(None, min_length=1, max_length=50)
    year: Optional[int] = Field(None, ge=2020, le=2030)
    license_plate: Optional[str] = Field(None, max_length=20)
    status: Optional[VehicleStatus] = None
    battery_capacity: Optional[Decimal] = Field(None, ge=0, le=999.99)


class VehicleResponse(VehicleBase):
    """Schema for vehicle response"""
    id: str
    status: VehicleStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Made with Bob
