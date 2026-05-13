"""
Database models package
"""
from app.models.vehicle import Vehicle
from app.models.telemetry import Telemetry
from app.models.fleet import FleetAssignment
from app.models.alert import Alert

__all__ = ["Vehicle", "Telemetry", "FleetAssignment", "Alert"]

# Made with Bob
