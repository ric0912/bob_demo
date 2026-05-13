"""
Vehicle API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from app.database import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.events import event_queue, Event, EventType

router = APIRouter()


@router.get("/vehicles", response_model=List[VehicleResponse])
async def list_vehicles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all vehicles with pagination
    """
    vehicles = db.query(Vehicle).offset(skip).limit(limit).all()
    return vehicles


@router.post("/vehicles", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle: VehicleCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new vehicle
    """
    # Check if VIN already exists
    existing = db.query(Vehicle).filter(Vehicle.vin == vehicle.vin).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vehicle with VIN {vehicle.vin} already exists"
        )
    
    # Create new vehicle
    db_vehicle = Vehicle(
        id=str(uuid.uuid4()),
        **vehicle.model_dump()
    )
    
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    
    # Publish event
    await event_queue.publish(Event(
        event_type=EventType.VEHICLE_REGISTERED,
        data={
            "id": db_vehicle.id,
            "vin": db_vehicle.vin,
            "make": db_vehicle.make,
            "model": db_vehicle.model
        },
        timestamp=datetime.utcnow(),
        event_id=str(uuid.uuid4())
    ))
    
    return db_vehicle


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db)
):
    """
    Get vehicle by ID
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found"
        )
    return vehicle


@router.put("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: str,
    vehicle_update: VehicleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update vehicle information
    """
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found"
        )
    
    # Track status change
    old_status = db_vehicle.status
    
    # Update fields
    update_data = vehicle_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_vehicle, field, value)
    
    db.commit()
    db.refresh(db_vehicle)
    
    # Publish status change event if status changed
    if old_status != db_vehicle.status:
        await event_queue.publish(Event(
            event_type=EventType.VEHICLE_STATUS_CHANGED,
            data={
                "vehicle_id": db_vehicle.id,
                "old_status": old_status.value,
                "new_status": db_vehicle.status.value
            },
            timestamp=datetime.utcnow(),
            event_id=str(uuid.uuid4())
        ))
    
    return db_vehicle


@router.delete("/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a vehicle
    """
    db_vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not db_vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found"
        )
    
    db.delete(db_vehicle)
    db.commit()
    return None


@router.get("/vehicles/{vehicle_id}/status")
async def get_vehicle_status(
    vehicle_id: str,
    db: Session = Depends(get_db)
):
    """
    Get vehicle status
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {vehicle_id} not found"
        )
    
    return {
        "vehicle_id": vehicle.id,
        "status": vehicle.status,
        "battery_capacity": vehicle.battery_capacity,
        "last_updated": vehicle.updated_at
    }

# Made with Bob
