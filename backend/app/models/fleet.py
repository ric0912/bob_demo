"""
Fleet assignment database model
"""
from sqlalchemy import Column, String, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
import enum


class AssignmentStatus(str, enum.Enum):
    """Fleet assignment status enumeration"""
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class FleetAssignment(Base):
    """Fleet assignment model for managing vehicle routes and tasks"""
    
    __tablename__ = "fleet_assignments"
    
    id = Column(String(36), primary_key=True, index=True)
    vehicle_id = Column(String(36), ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(String(36), nullable=True)
    route_id = Column(String(36))
    assigned_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(
        Enum(AssignmentStatus),
        default=AssignmentStatus.ASSIGNED,
        nullable=False
    )
    
    def __repr__(self):
        return f"<FleetAssignment(id={self.id}, vehicle_id={self.vehicle_id}, status={self.status})>"

# Made with Bob
