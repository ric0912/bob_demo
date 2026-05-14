"""
Telemetry database model
"""
from sqlalchemy import Column, String, Integer, DECIMAL, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from app.database import Base


class Telemetry(Base):
    """Telemetry model for storing vehicle sensor data"""
    
    __tablename__ = "telemetry"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id"), nullable=False)
    latitude = Column(DECIMAL(10, 8), nullable=False)
    longitude = Column(DECIMAL(11, 8), nullable=False)
    speed = Column(DECIMAL(5, 2))
    battery_level = Column(DECIMAL(5, 2))
    heading = Column(DECIMAL(5, 2))
    odometer = Column(DECIMAL(10, 2))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Create composite index for efficient queries
    __table_args__ = (
        Index('idx_vehicle_timestamp', 'vehicle_id', 'timestamp'),
    )
    
    def __repr__(self):
        return f"<Telemetry(id={self.id}, vehicle_id={self.vehicle_id}, timestamp={self.timestamp})>"

# Made with Bob
