"""
Seed dummy data for demo purposes
"""
import logging
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.telemetry import Telemetry
from app.models.fleet import FleetAssignment
from app.models.alert import Alert

logger = logging.getLogger(__name__)


def generate_dummy_data(db: Session) -> None:
    """
    Generate dummy data for demo purposes
    
    Args:
        db: Database session
    """
    logger.info("Generating dummy data...")
    
    # Check if data already exists
    existing_vehicles = db.query(Vehicle).count()
    if existing_vehicles > 0:
        logger.info(f"Database already has {existing_vehicles} vehicles. Skipping data generation.")
        return
    
    # Vehicle makes and models
    vehicle_types = [
        ("Tesla", "Model 3"),
        ("Tesla", "Model Y"),
        ("Waymo", "Jaguar I-PACE"),
        ("Cruise", "Chevy Bolt"),
        ("Zoox", "Robotaxi"),
        ("Aurora", "Pacifica"),
        ("Nuro", "R2"),
        ("Tesla", "Cybertruck"),
    ]
    
    # Generate 10 vehicles
    vehicles = []
    for i in range(10):
        make, model = random.choice(vehicle_types)
        vehicle = Vehicle(
            vin=f"VIN{i+1:03d}{''.join([str(random.randint(0, 9)) for _ in range(14)])}",
            make=make,
            model=model,
            year=random.randint(2020, 2024),
            license_plate=f"AV{i+1:04d}",
            status=random.choice(["active", "idle", "maintenance"]),
            battery_capacity=random.uniform(75.0, 100.0)
        )
        db.add(vehicle)
        vehicles.append(vehicle)
    
    db.commit()
    logger.info(f"Created {len(vehicles)} vehicles")
    
    # Generate telemetry data for each vehicle
    telemetry_count = 0
    base_locations = [
        (37.7749, -122.4194),  # San Francisco
        (34.0522, -118.2437),  # Los Angeles
        (40.7128, -74.0060),   # New York
        (41.8781, -87.6298),   # Chicago
        (29.7604, -95.3698),   # Houston
    ]
    
    for vehicle in vehicles:
        # Generate 5 telemetry records per vehicle
        base_lat, base_lon = random.choice(base_locations)
        
        for j in range(5):
            timestamp = datetime.utcnow() - timedelta(hours=5-j)
            telemetry = Telemetry(
                vehicle_id=vehicle.id,
                latitude=base_lat + random.uniform(-0.1, 0.1),
                longitude=base_lon + random.uniform(-0.1, 0.1),
                speed=random.uniform(0, 65) if vehicle.status == "active" else 0,
                battery_level=random.uniform(20, 100),
                heading=random.uniform(0, 360),
                odometer=random.uniform(1000, 50000),
                timestamp=timestamp
            )
            db.add(telemetry)
            telemetry_count += 1
    
    db.commit()
    logger.info(f"Created {telemetry_count} telemetry records")
    
    # Generate fleet assignments for active vehicles
    assignment_count = 0
    active_vehicles = [v for v in vehicles if v.status == "active"]
    
    for vehicle in active_vehicles[:5]:  # Assign 5 vehicles
        assignment = FleetAssignment(
            vehicle_id=vehicle.id,
            route_id=f"ROUTE{random.randint(100, 999)}",
            status=random.choice(["assigned", "in_progress"]),
            assigned_at=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
        )
        db.add(assignment)
        assignment_count += 1
    
    db.commit()
    logger.info(f"Created {assignment_count} fleet assignments")
    
    # Generate some alerts
    alert_count = 0
    alert_types = ["battery_low", "maintenance_required", "sensor_failure", "system_error"]
    severities = ["low", "medium", "high"]
    
    for vehicle in random.sample(vehicles, min(3, len(vehicles))):
        alert = Alert(
            vehicle_id=vehicle.id,
            alert_type=random.choice(alert_types),
            severity=random.choice(severities),
            message=f"Alert for vehicle {vehicle.license_plate}",
            acknowledged=random.choice([True, False])
        )
        db.add(alert)
        alert_count += 1
    
    db.commit()
    logger.info(f"Created {alert_count} alerts")
    
    logger.info("Dummy data generation complete!")
    logger.info(f"Summary: {len(vehicles)} vehicles, {telemetry_count} telemetry records, "
                f"{assignment_count} assignments, {alert_count} alerts")

# Made with Bob
