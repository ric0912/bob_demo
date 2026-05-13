"""
Telemetry API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from app.database import get_db
from app.models.telemetry import Telemetry
from app.models.vehicle import Vehicle
from app.schemas.telemetry import TelemetryCreate, TelemetryResponse
from app.events import event_queue, Event, EventType

router = APIRouter()


@router.get("/telemetry", response_model=List[TelemetryResponse])
async def list_telemetry(
    vehicle_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List telemetry data with optional vehicle filter
    """
    query = db.query(Telemetry)
    
    if vehicle_id:
        query = query.filter(Telemetry.vehicle_id == vehicle_id)
    
    telemetry = query.order_by(Telemetry.timestamp.desc()).offset(skip).limit(limit).all()
    return telemetry


@router.post("/telemetry", response_model=TelemetryResponse, status_code=status.HTTP_201_CREATED)
async def create_telemetry(
    telemetry: TelemetryCreate,
    db: Session = Depends(get_db)
):
    """
    Submit telemetry data for a vehicle
    """
    # Verify vehicle exists
    vehicle = db.query(Vehicle).filter(Vehicle.id == telemetry.vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {telemetry.vehicle_id} not found"
        )
    
    # Create telemetry record
    db_telemetry = Telemetry(**telemetry.model_dump())
    
    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)
    
    # Publish event
    await event_queue.publish(Event(
        event_type=EventType.TELEMETRY_RECEIVED,
        data={
            "vehicle_id": db_telemetry.vehicle_id,
            "latitude": float(db_telemetry.latitude),
            "longitude": float(db_telemetry.longitude),
            "speed": float(db_telemetry.speed) if db_telemetry.speed else None,
            "battery_level": float(db_telemetry.battery_level) if db_telemetry.battery_level else None,
            "timestamp": db_telemetry.timestamp.isoformat()
        },
        timestamp=datetime.utcnow(),
        event_id=str(uuid.uuid4())
    ))
    
    return db_telemetry


@router.get("/telemetry/vehicle/{vehicle_id}", response_model=List[TelemetryResponse])
async def get_vehicle_telemetry(
    vehicle_id: str,
    limit: int = Query(default=100, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get telemetry history for a specific vehicle
    """
    # Verify vehicle exists
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found"
        )
    
    telemetry = db.query(Telemetry)\
        .filter(Telemetry.vehicle_id == vehicle_id)\
        .order_by(Telemetry.timestamp.desc())\
        .limit(limit)\
        .all()
    
    return telemetry


@router.get("/telemetry/latest")
async def get_latest_telemetry(
    db: Session = Depends(get_db)
):
    """
    Get latest telemetry for all active vehicles
    """
    # Get all active vehicles
    vehicles = db.query(Vehicle).all()
    
    result = []
    for vehicle in vehicles:
        latest = db.query(Telemetry)\
            .filter(Telemetry.vehicle_id == vehicle.id)\
            .order_by(Telemetry.timestamp.desc())\
            .first()
        
        if latest:
            result.append({
                "vehicle_id": vehicle.id,
                "vin": vehicle.vin,
                "status": vehicle.status,
                "telemetry": {
                    "latitude": float(latest.latitude),
                    "longitude": float(latest.longitude),
                    "speed": float(latest.speed) if latest.speed else None,
                    "battery_level": float(latest.battery_level) if latest.battery_level else None,
                    "timestamp": latest.timestamp
                }
            })
    
    return result

# Made with Bob
