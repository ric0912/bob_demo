"""
Fleet management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import uuid
from datetime import datetime

from app.database import get_db
from app.models.fleet import FleetAssignment, AssignmentStatus
from app.models.alert import Alert, AlertSeverity
from app.models.vehicle import Vehicle, VehicleStatus
from app.schemas.fleet import FleetAssignmentCreate, FleetAssignmentUpdate, FleetAssignmentResponse
from app.schemas.alert import AlertResponse
from app.events import event_queue, Event, EventType

router = APIRouter()


@router.get("/fleet/overview")
async def get_fleet_overview(db: Session = Depends(get_db)):
    """
    Get fleet overview statistics
    """
    # Count vehicles by status
    vehicle_stats = db.query(
        Vehicle.status,
        func.count(Vehicle.id).label('count')
    ).group_by(Vehicle.status).all()
    
    # Count active assignments
    active_assignments = db.query(FleetAssignment)\
        .filter(FleetAssignment.status.in_([
            AssignmentStatus.ASSIGNED,
            AssignmentStatus.IN_PROGRESS
        ])).count()
    
    # Count unacknowledged alerts by severity
    alert_stats = db.query(
        Alert.severity,
        func.count(Alert.id).label('count')
    ).filter(Alert.acknowledged == False)\
     .group_by(Alert.severity).all()
    
    return {
        "total_vehicles": db.query(Vehicle).count(),
        "vehicle_status": {stat.status.value: stat.count for stat in vehicle_stats},
        "active_assignments": active_assignments,
        "unacknowledged_alerts": {stat.severity.value: stat.count for stat in alert_stats}
    }


@router.get("/fleet/assignments", response_model=List[FleetAssignmentResponse])
async def list_assignments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all fleet assignments
    """
    assignments = db.query(FleetAssignment)\
        .order_by(FleetAssignment.assigned_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    return assignments


@router.post("/fleet/assignments", response_model=FleetAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment: FleetAssignmentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new fleet assignment
    """
    # Verify vehicle exists
    vehicle = db.query(Vehicle).filter(Vehicle.id == assignment.vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle {assignment.vehicle_id} not found"
        )
    
    # Check if vehicle is available
    if vehicle.status not in [VehicleStatus.IDLE, VehicleStatus.ACTIVE]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vehicle {assignment.vehicle_id} is not available (status: {vehicle.status})"
        )
    
    # Create assignment
    db_assignment = FleetAssignment(
        id=str(uuid.uuid4()),
        **assignment.model_dump()
    )
    
    db.add(db_assignment)
    
    # Update vehicle status
    vehicle.status = VehicleStatus.ACTIVE
    
    db.commit()
    db.refresh(db_assignment)
    
    # Publish event
    await event_queue.publish(Event(
        event_type=EventType.ASSIGNMENT_CREATED,
        data={
            "assignment_id": db_assignment.id,
            "vehicle_id": db_assignment.vehicle_id,
            "route_id": db_assignment.route_id
        },
        timestamp=datetime.utcnow(),
        event_id=str(uuid.uuid4())
    ))
    
    return db_assignment


@router.put("/fleet/assignments/{assignment_id}", response_model=FleetAssignmentResponse)
async def update_assignment(
    assignment_id: str,
    assignment_update: FleetAssignmentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a fleet assignment
    """
    db_assignment = db.query(FleetAssignment)\
        .filter(FleetAssignment.id == assignment_id)\
        .first()
    
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment {assignment_id} not found"
        )
    
    # Update fields
    update_data = assignment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assignment, field, value)
    
    # If status is completed, set completed_at
    if db_assignment.status == AssignmentStatus.COMPLETED:
        db_assignment.completed_at = datetime.utcnow()
        
        # Update vehicle status to idle
        vehicle = db.query(Vehicle).filter(Vehicle.id == db_assignment.vehicle_id).first()
        if vehicle:
            vehicle.status = VehicleStatus.IDLE
        
        # Publish event
        await event_queue.publish(Event(
            event_type=EventType.ASSIGNMENT_COMPLETED,
            data={
                "assignment_id": db_assignment.id,
                "vehicle_id": db_assignment.vehicle_id
            },
            timestamp=datetime.utcnow(),
            event_id=str(uuid.uuid4())
        ))
    
    db.commit()
    db.refresh(db_assignment)
    
    return db_assignment


@router.get("/fleet/alerts", response_model=List[AlertResponse])
async def list_alerts(
    acknowledged: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List fleet alerts
    """
    query = db.query(Alert)
    
    if not acknowledged:
        query = query.filter(Alert.acknowledged == False)
    
    alerts = query.order_by(Alert.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return alerts


@router.post("/fleet/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    db: Session = Depends(get_db)
):
    """
    Acknowledge an alert
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert {alert_id} not found"
        )
    
    alert.acknowledged = True
    db.commit()
    
    return {"message": "Alert acknowledged", "alert_id": alert_id}

# Made with Bob
