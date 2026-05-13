"""
Pydantic schemas for request/response validation
"""
from app.schemas.vehicle import (
    VehicleBase,
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse
)
from app.schemas.telemetry import (
    TelemetryBase,
    TelemetryCreate,
    TelemetryResponse
)
from app.schemas.fleet import (
    FleetAssignmentBase,
    FleetAssignmentCreate,
    FleetAssignmentUpdate,
    FleetAssignmentResponse
)
from app.schemas.alert import (
    AlertBase,
    AlertCreate,
    AlertResponse
)

__all__ = [
    "VehicleBase",
    "VehicleCreate",
    "VehicleUpdate",
    "VehicleResponse",
    "TelemetryBase",
    "TelemetryCreate",
    "TelemetryResponse",
    "FleetAssignmentBase",
    "FleetAssignmentCreate",
    "FleetAssignmentUpdate",
    "FleetAssignmentResponse",
    "AlertBase",
    "AlertCreate",
    "AlertResponse"
]

# Made with Bob
