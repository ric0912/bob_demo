"""
Alert Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.alert import AlertType, AlertSeverity


class AlertBase(BaseModel):
    """Base alert schema"""
    vehicle_id: str = Field(..., min_length=1, max_length=36)
    alert_type: AlertType
    severity: AlertSeverity
    message: Optional[str] = None


class AlertCreate(AlertBase):
    """Schema for creating an alert"""
    pass


class AlertResponse(AlertBase):
    """Schema for alert response"""
    id: str
    acknowledged: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Made with Bob
