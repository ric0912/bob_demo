"""
Analytics API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.models.vehicle import Vehicle, VehicleStatus
from app.models.telemetry import Telemetry
from app.models.fleet import FleetAssignment, AssignmentStatus
from app.models.alert import Alert, AlertSeverity

router = APIRouter()


@router.get("/analytics/summary")
async def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Get overall analytics summary
    """
    # Total vehicles
    total_vehicles = db.query(Vehicle).count()
    
    # Active vehicles
    active_vehicles = db.query(Vehicle)\
        .filter(Vehicle.status == VehicleStatus.ACTIVE)\
        .count()
    
    # Total telemetry records
    total_telemetry = db.query(Telemetry).count()
    
    # Completed assignments (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    completed_assignments = db.query(FleetAssignment)\
        .filter(
            and_(
                FleetAssignment.status == AssignmentStatus.COMPLETED,
                FleetAssignment.completed_at >= thirty_days_ago
            )
        ).count()
    
    # Critical alerts (unacknowledged)
    critical_alerts = db.query(Alert)\
        .filter(
            and_(
                Alert.severity == AlertSeverity.CRITICAL,
                Alert.acknowledged == False
            )
        ).count()
    
    # Average battery level
    avg_battery = db.query(func.avg(Telemetry.battery_level))\
        .filter(Telemetry.battery_level.isnot(None))\
        .scalar()
    
    return {
        "total_vehicles": total_vehicles,
        "active_vehicles": active_vehicles,
        "total_telemetry_records": total_telemetry,
        "completed_assignments_30d": completed_assignments,
        "critical_alerts": critical_alerts,
        "average_battery_level": float(avg_battery) if avg_battery else None
    }


@router.get("/analytics/vehicle/{vehicle_id}")
async def get_vehicle_analytics(
    vehicle_id: str,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get analytics for a specific vehicle
    """
    # Verify vehicle exists
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail=f"Vehicle {vehicle_id} not found"
        )
    
    # Date range
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Telemetry count
    telemetry_count = db.query(Telemetry)\
        .filter(
            and_(
                Telemetry.vehicle_id == vehicle_id,
                Telemetry.timestamp >= start_date
            )
        ).count()
    
    # Average speed
    avg_speed = db.query(func.avg(Telemetry.speed))\
        .filter(
            and_(
                Telemetry.vehicle_id == vehicle_id,
                Telemetry.timestamp >= start_date,
                Telemetry.speed.isnot(None)
            )
        ).scalar()
    
    # Total distance (approximate from odometer)
    distance_data = db.query(
        func.min(Telemetry.odometer).label('min_odo'),
        func.max(Telemetry.odometer).label('max_odo')
    ).filter(
        and_(
            Telemetry.vehicle_id == vehicle_id,
            Telemetry.timestamp >= start_date,
            Telemetry.odometer.isnot(None)
        )
    ).first()
    
    total_distance = None
    if distance_data and distance_data.min_odo and distance_data.max_odo:
        total_distance = float(distance_data.max_odo - distance_data.min_odo)
    
    # Assignments completed
    assignments_completed = db.query(FleetAssignment)\
        .filter(
            and_(
                FleetAssignment.vehicle_id == vehicle_id,
                FleetAssignment.status == AssignmentStatus.COMPLETED,
                FleetAssignment.completed_at >= start_date
            )
        ).count()
    
    # Alerts generated
    alerts_count = db.query(Alert)\
        .filter(
            and_(
                Alert.vehicle_id == vehicle_id,
                Alert.created_at >= start_date
            )
        ).count()
    
    return {
        "vehicle_id": vehicle_id,
        "vin": vehicle.vin,
        "period_days": days,
        "telemetry_records": telemetry_count,
        "average_speed": float(avg_speed) if avg_speed else None,
        "total_distance": total_distance,
        "assignments_completed": assignments_completed,
        "alerts_generated": alerts_count
    }


@router.get("/analytics/performance")
async def get_performance_metrics(
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get fleet performance metrics
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Average assignment completion time
    # SQLite-compatible: use julianday to calculate difference in seconds
    completed = db.query(
        func.avg(
            (func.julianday(FleetAssignment.completed_at) -
             func.julianday(FleetAssignment.assigned_at)) * 86400
        ).label('avg_seconds')
    ).filter(
        and_(
            FleetAssignment.status == AssignmentStatus.COMPLETED,
            FleetAssignment.completed_at >= start_date
        )
    ).scalar()
    
    avg_completion_time = float(completed) if completed else None
    
    # Vehicle utilization rate
    total_vehicles = db.query(Vehicle).count()
    active_time = db.query(func.count(Vehicle.id))\
        .filter(Vehicle.status == VehicleStatus.ACTIVE)\
        .scalar()
    
    utilization_rate = (active_time / total_vehicles * 100) if total_vehicles > 0 else 0
    
    # Alert rate
    total_alerts = db.query(Alert)\
        .filter(Alert.created_at >= start_date)\
        .count()
    
    alert_rate = total_alerts / days if days > 0 else 0
    
    return {
        "period_days": days,
        "avg_assignment_completion_seconds": avg_completion_time,
        "vehicle_utilization_rate": utilization_rate,
        "alerts_per_day": alert_rate
    }


@router.get("/analytics/trends")
async def get_trends(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get trend analysis data
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily telemetry count
    daily_telemetry = db.query(
        func.date(Telemetry.timestamp).label('date'),
        func.count(Telemetry.id).label('count')
    ).filter(Telemetry.timestamp >= start_date)\
     .group_by(func.date(Telemetry.timestamp))\
     .order_by(func.date(Telemetry.timestamp))\
     .all()
    
    # Daily assignments
    daily_assignments = db.query(
        func.date(FleetAssignment.assigned_at).label('date'),
        func.count(FleetAssignment.id).label('count')
    ).filter(FleetAssignment.assigned_at >= start_date)\
     .group_by(func.date(FleetAssignment.assigned_at))\
     .order_by(func.date(FleetAssignment.assigned_at))\
     .all()
    
    # Daily alerts
    daily_alerts = db.query(
        func.date(Alert.created_at).label('date'),
        func.count(Alert.id).label('count')
    ).filter(Alert.created_at >= start_date)\
     .group_by(func.date(Alert.created_at))\
     .order_by(func.date(Alert.created_at))\
     .all()
    
    return {
        "period_days": days,
        "telemetry_trend": [
            {"date": str(item.date), "count": item.count}
            for item in daily_telemetry
        ],
        "assignments_trend": [
            {"date": str(item.date), "count": item.count}
            for item in daily_assignments
        ],
        "alerts_trend": [
            {"date": str(item.date), "count": item.count}
            for item in daily_alerts
        ]
    }

# Made with Bob
