"""
Fleet assignment Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.fleet import AssignmentStatus


class FleetAssignmentBase(BaseModel):
    """Base fleet assignment schema"""
    vehicle_id: str = Field(..., min_length=1, max_length=36)
    route_id: Optional[str] = Field(None, max_length=36)


class FleetAssignmentCreate(FleetAssignmentBase):
    """Schema for creating a fleet assignment"""
    pass


class FleetAssignmentUpdate(BaseModel):
    """Schema for updating a fleet assignment"""
    route_id: Optional[str] = Field(None, max_length=36)
    status: Optional[AssignmentStatus] = None


class FleetAssignmentResponse(FleetAssignmentBase):
    """Schema for fleet assignment response"""
    id: str
    status: AssignmentStatus
    assigned_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Made with Bob
