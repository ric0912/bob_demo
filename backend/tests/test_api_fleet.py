"""
Unit tests for Fleet Management API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

from app.models.vehicle import Vehicle, VehicleStatus
from app.models.fleet import FleetAssignment, AssignmentStatus
from app.models.alert import Alert, AlertSeverity, AlertType


@pytest.mark.api
@pytest.mark.unit
class TestFleetAPI:
    """Test suite for fleet management API endpoints"""
    
    def test_get_fleet_overview_empty(self, client: TestClient):
        """Test fleet overview with empty database"""
        response = client.get("/api/v1/fleet/overview")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_vehicles"] == 0
        assert data["active_assignments"] == 0
    
    def test_get_fleet_overview_with_data(self, client: TestClient, db: Session):
        """Test fleet overview with vehicles and assignments"""
        # Create vehicles
        vehicle1 = Vehicle(
            id="vehicle-1",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.ACTIVE
        )
        vehicle2 = Vehicle(
            id="vehicle-2",
            vin="1HGBH41JXMN109187",
            make="Tesla",
            model="Model Y",
            year=2023,
            status=VehicleStatus.IDLE
        )
        db.add_all([vehicle1, vehicle2])
        db.commit()
        
        # Create assignment
        assignment = FleetAssignment(
            id=str(uuid.uuid4()),
            vehicle_id="vehicle-1",
            route_id="route-123",
            driver_id="driver-456",
            status=AssignmentStatus.IN_PROGRESS
        )
        db.add(assignment)
        db.commit()
        
        # Get overview
        response = client.get("/api/v1/fleet/overview")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_vehicles"] == 2
        assert data["active_assignments"] == 1
        assert "vehicle_status" in data
    
    def test_list_assignments_empty(self, client: TestClient):
        """Test listing assignments when database is empty"""
        response = client.get("/api/v1/fleet/assignments")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_assignment_success(self, client: TestClient, db: Session, sample_fleet_assignment_data):
        """Test successful assignment creation"""
        # Create vehicle
        vehicle = Vehicle(
            id=sample_fleet_assignment_data["vehicle_id"],
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.IDLE
        )
        db.add(vehicle)
        db.commit()
        
        # Create assignment
        response = client.post("/api/v1/fleet/assignments", json=sample_fleet_assignment_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["vehicle_id"] == sample_fleet_assignment_data["vehicle_id"]
        assert data["route_id"] == sample_fleet_assignment_data["route_id"]
        assert data["driver_id"] == sample_fleet_assignment_data["driver_id"]
        assert "id" in data
        assert "assigned_at" in data
    
    def test_create_assignment_vehicle_not_found(self, client: TestClient, sample_fleet_assignment_data):
        """Test creating assignment for non-existent vehicle"""
        response = client.post("/api/v1/fleet/assignments", json=sample_fleet_assignment_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_create_assignment_vehicle_unavailable(self, client: TestClient, db: Session):
        """Test creating assignment for unavailable vehicle"""
        # Create vehicle in maintenance
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.MAINTENANCE
        )
        db.add(vehicle)
        db.commit()
        
        assignment_data = {
            "vehicle_id": "test-vehicle-id",
            "route_id": "route-123",
            "driver_id": "driver-456",
            "status": "assigned"
        }
        
        response = client.post("/api/v1/fleet/assignments", json=assignment_data)
        assert response.status_code == 400
        assert "not available" in response.json()["detail"].lower()
    
    def test_update_assignment_success(self, client: TestClient, db: Session):
        """Test updating assignment"""
        # Create vehicle and assignment
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.ACTIVE
        )
        db.add(vehicle)
        
        assignment = FleetAssignment(
            id="assignment-1",
            vehicle_id="test-vehicle-id",
            route_id="route-123",
            driver_id="driver-456",
            status=AssignmentStatus.ASSIGNED
        )
        db.add(assignment)
        db.commit()
        
        # Update assignment
        update_data = {"status": "in_progress"}
        response = client.put("/api/v1/fleet/assignments/assignment-1", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "in_progress"
    
    def test_update_assignment_to_completed(self, client: TestClient, db: Session):
        """Test completing an assignment"""
        # Create vehicle and assignment
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.ACTIVE
        )
        db.add(vehicle)
        
        assignment = FleetAssignment(
            id="assignment-1",
            vehicle_id="test-vehicle-id",
            route_id="route-123",
            driver_id="driver-456",
            status=AssignmentStatus.IN_PROGRESS
        )
        db.add(assignment)
        db.commit()
        
        # Complete assignment
        update_data = {"status": "completed"}
        response = client.put("/api/v1/fleet/assignments/assignment-1", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "completed"
        assert data["completed_at"] is not None
        
        # Verify vehicle status changed to idle
        db.refresh(vehicle)
        assert vehicle.status == VehicleStatus.IDLE
    
    def test_update_assignment_not_found(self, client: TestClient):
        """Test updating non-existent assignment"""
        fake_id = str(uuid.uuid4())
        update_data = {"status": "completed"}
        response = client.put(f"/api/v1/fleet/assignments/{fake_id}", json=update_data)
        assert response.status_code == 404
    
    def test_list_alerts_empty(self, client: TestClient):
        """Test listing alerts when database is empty"""
        response = client.get("/api/v1/fleet/alerts")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_alerts_unacknowledged_only(self, client: TestClient, db: Session):
        """Test listing only unacknowledged alerts"""
        # Create vehicle
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.ACTIVE
        )
        db.add(vehicle)
        
        # Create alerts
        alert1 = Alert(
            id="alert-1",
            vehicle_id="test-vehicle-id",
            alert_type=AlertType.BATTERY_LOW,
            severity=AlertSeverity.HIGH,
            message="Battery low",
            acknowledged=False
        )
        alert2 = Alert(
            id="alert-2",
            vehicle_id="test-vehicle-id",
            alert_type=AlertType.MAINTENANCE_REQUIRED,
            severity=AlertSeverity.LOW,
            message="Maintenance due",
            acknowledged=True
        )
        db.add_all([alert1, alert2])
        db.commit()
        
        # Get unacknowledged alerts
        response = client.get("/api/v1/fleet/alerts?acknowledged=false")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["acknowledged"] is False
    
    def test_acknowledge_alert_success(self, client: TestClient, db: Session):
        """Test acknowledging an alert"""
        # Create vehicle and alert
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.ACTIVE
        )
        db.add(vehicle)
        
        alert = Alert(
            id="alert-1",
            vehicle_id="test-vehicle-id",
            alert_type=AlertType.BATTERY_LOW,
            severity=AlertSeverity.HIGH,
            message="Battery low",
            acknowledged=False
        )
        db.add(alert)
        db.commit()
        
        # Acknowledge alert
        response = client.post("/api/v1/fleet/alerts/alert-1/acknowledge")
        assert response.status_code == 200
        assert response.json()["message"] == "Alert acknowledged"
        
        # Verify alert is acknowledged
        db.refresh(alert)
        assert alert.acknowledged is True
    
    def test_acknowledge_alert_not_found(self, client: TestClient):
        """Test acknowledging non-existent alert"""
        fake_id = str(uuid.uuid4())
        response = client.post(f"/api/v1/fleet/alerts/{fake_id}/acknowledge")
        assert response.status_code == 404
    
    def test_list_assignments_with_pagination(self, client: TestClient, db: Session):
        """Test listing assignments with pagination"""
        # Create vehicle
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.IDLE
        )
        db.add(vehicle)
        db.commit()
        
        # Create multiple assignments
        for i in range(5):
            assignment = FleetAssignment(
                id=f"assignment-{i}",
                vehicle_id="test-vehicle-id",
                route_id=f"route-{i}",
                driver_id=f"driver-{i}",
                status=AssignmentStatus.COMPLETED
            )
            db.add(assignment)
        db.commit()
        
        # Test pagination
        response = client.get("/api/v1/fleet/assignments?skip=0&limit=3")
        assert response.status_code == 200
        assert len(response.json()) == 3
        
        response = client.get("/api/v1/fleet/assignments?skip=3&limit=3")
        assert response.status_code == 200
        assert len(response.json()) == 2


@pytest.mark.database
class TestFleetDatabase:
    """Test fleet database operations"""
    
    def test_fleet_assignment_model_creation(self, db: Session):
        """Test creating fleet assignment model"""
        # Create vehicle
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.IDLE
        )
        db.add(vehicle)
        db.commit()
        
        # Create assignment
        assignment = FleetAssignment(
            id=str(uuid.uuid4()),
            vehicle_id="test-vehicle-id",
            route_id="route-123",
            driver_id="driver-456",
            status=AssignmentStatus.ASSIGNED
        )
        
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        
        assert assignment.id is not None
        assert assignment.assigned_at is not None
    
    def test_alert_model_creation(self, db: Session):
        """Test creating alert model"""
        # Create vehicle
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.ACTIVE
        )
        db.add(vehicle)
        db.commit()
        
        # Create alert
        alert = Alert(
            id=str(uuid.uuid4()),
            vehicle_id="test-vehicle-id",
            alert_type=AlertType.BATTERY_LOW,
            severity=AlertSeverity.CRITICAL,
            message="Battery critically low",
            acknowledged=False
        )
        
        db.add(alert)
        db.commit()
        db.refresh(alert)
        
        assert alert.id is not None
        assert alert.created_at is not None
        assert alert.acknowledged is False

# Made with Bob
