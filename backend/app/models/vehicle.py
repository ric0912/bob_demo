"""
Vehicle database model
"""
from sqlalchemy import Column, String, Integer, Enum, DECIMAL, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum


class VehicleStatus(str, enum.Enum):
    """Vehicle status enumeration"""
    ACTIVE = "active"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class Vehicle(Base):
    """Vehicle model representing autonomous vehicles in the fleet"""
    
    __tablename__ = "vehicles"
    
    id = Column(String(36), primary_key=True, index=True)
    vin = Column(String(17), unique=True, nullable=False, index=True)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)
    license_plate = Column(String(20))
    status = Column(
        Enum(VehicleStatus),
        default=VehicleStatus.IDLE,
        nullable=False
    )
    battery_capacity = Column(DECIMAL(5, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    def __repr__(self):
        return f"<Vehicle(id={self.id}, vin={self.vin}, status={self.status})>"

# Made with Bob
