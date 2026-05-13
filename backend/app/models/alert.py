"""
Alert database model
"""
from sqlalchemy import Column, String, Enum, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from app.database import Base
import enum


class AlertType(str, enum.Enum):
    """Alert type enumeration"""
    BATTERY_LOW = "battery_low"
    MAINTENANCE_REQUIRED = "maintenance_required"
    SENSOR_FAILURE = "sensor_failure"
    SYSTEM_ERROR = "system_error"


class AlertSeverity(str, enum.Enum):
    """Alert severity enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Alert(Base):
    """Alert model for tracking vehicle alerts and notifications"""
    
    __tablename__ = "alerts"
    
    id = Column(String(36), primary_key=True, index=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id"), nullable=False)
    alert_type = Column(Enum(AlertType), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)
    message = Column(Text)
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Create composite index for efficient queries
    __table_args__ = (
        Index('idx_vehicle_severity', 'vehicle_id', 'severity'),
    )
    
    def __repr__(self):
        return f"<Alert(id={self.id}, vehicle_id={self.vehicle_id}, type={self.alert_type}, severity={self.severity})>"

# Made with Bob
