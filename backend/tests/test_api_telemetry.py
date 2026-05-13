"""
Unit tests for Telemetry API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.models.vehicle import Vehicle, VehicleStatus
from app.models.telemetry import Telemetry


@pytest.mark.api
@pytest.mark.unit
class TestTelemetryAPI:
    """Test suite for telemetry API endpoints"""
    
    def test_list_telemetry_empty(self, client: TestClient):
        """Test listing telemetry when database is empty"""
        response = client.get("/api/v1/telemetry")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_telemetry_success(self, client: TestClient, db: Session, sample_vehicle_data, sample_telemetry_data):
        """Test successful telemetry creation"""
        # Create vehicle first
        vehicle = Vehicle(
            id=sample_telemetry_data["vehicle_id"],
            vin=sample_vehicle_data["vin"],
            make=sample_vehicle_data["make"],
            model=sample_vehicle_data["model"],
            year=sample_vehicle_data["year"],
            status=VehicleStatus.IDLE
        )
        db.add(vehicle)
        db.commit()
        
        # Create telemetry
        response = client.post("/api/v1/telemetry", json=sample_telemetry_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["vehicle_id"] == sample_telemetry_data["vehicle_id"]
        assert float(data["latitude"]) == sample_telemetry_data["latitude"]
        assert float(data["longitude"]) == sample_telemetry_data["longitude"]
        assert float(data["speed"]) == sample_telemetry_data["speed"]
        assert float(data["battery_level"]) == sample_telemetry_data["battery_level"]
    
    def test_create_telemetry_vehicle_not_found(self, client: TestClient, sample_telemetry_data):
        """Test creating telemetry for non-existent vehicle"""
        response = client.post("/api/v1/telemetry", json=sample_telemetry_data)
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_create_telemetry_invalid_data(self, client: TestClient, db: Session, sample_vehicle_data):
        """Test creating telemetry with invalid data"""
        # Create vehicle
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin=sample_vehicle_data["vin"],
            make=sample_vehicle_data["make"],
            model=sample_vehicle_data["model"],
            year=sample_vehicle_data["year"],
            status=VehicleStatus.IDLE
        )
        db.add(vehicle)
        db.commit()
        
        invalid_data = {
            "vehicle_id": "test-vehicle-id",
            "latitude": 200.0,  # Invalid latitude
            "longitude": -122.4194
        }
        response = client.post("/api/v1/telemetry", json=invalid_data)
        assert response.status_code == 422
    
    def test_list_telemetry_with_vehicle_filter(self, client: TestClient, db: Session, sample_vehicle_data):
        """Test listing telemetry filtered by vehicle"""
        # Create two vehicles
        vehicle1 = Vehicle(
            id="vehicle-1",
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.IDLE
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
        
        # Create telemetry for both
        telemetry_data_1 = {
            "vehicle_id": "vehicle-1",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed": 45.5,
            "battery_level": 85.0
        }
        telemetry_data_2 = {
            "vehicle_id": "vehicle-2",
            "latitude": 37.7750,
            "longitude": -122.4195,
            "speed": 50.0,
            "battery_level": 90.0
        }
        
        client.post("/api/v1/telemetry", json=telemetry_data_1)
        client.post("/api/v1/telemetry", json=telemetry_data_2)
        
        # Filter by vehicle-1
        response = client.get("/api/v1/telemetry?vehicle_id=vehicle-1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["vehicle_id"] == "vehicle-1"
    
    def test_get_vehicle_telemetry(self, client: TestClient, db: Session, sample_vehicle_data):
        """Test getting telemetry history for specific vehicle"""
        # Create vehicle
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin=sample_vehicle_data["vin"],
            make=sample_vehicle_data["make"],
            model=sample_vehicle_data["model"],
            year=sample_vehicle_data["year"],
            status=VehicleStatus.IDLE
        )
        db.add(vehicle)
        db.commit()
        
        # Create multiple telemetry records
        for i in range(3):
            telemetry_data = {
                "vehicle_id": "test-vehicle-id",
                "latitude": 37.7749 + i * 0.001,
                "longitude": -122.4194 + i * 0.001,
                "speed": 45.5 + i,
                "battery_level": 85.0 - i
            }
            client.post("/api/v1/telemetry", json=telemetry_data)
        
        # Get vehicle telemetry
        response = client.get("/api/v1/telemetry/vehicle/test-vehicle-id")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(item["vehicle_id"] == "test-vehicle-id" for item in data)
    
    def test_get_vehicle_telemetry_not_found(self, client: TestClient):
        """Test getting telemetry for non-existent vehicle"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/telemetry/vehicle/{fake_id}")
        assert response.status_code == 404
    
    def test_get_vehicle_telemetry_with_limit(self, client: TestClient, db: Session, sample_vehicle_data):
        """Test getting telemetry with limit parameter"""
        # Create vehicle
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin=sample_vehicle_data["vin"],
            make=sample_vehicle_data["make"],
            model=sample_vehicle_data["model"],
            year=sample_vehicle_data["year"],
            status=VehicleStatus.IDLE
        )
        db.add(vehicle)
        db.commit()
        
        # Create 10 telemetry records
        for i in range(10):
            telemetry_data = {
                "vehicle_id": "test-vehicle-id",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed": 45.5,
                "battery_level": 85.0
            }
            client.post("/api/v1/telemetry", json=telemetry_data)
        
        # Get with limit
        response = client.get("/api/v1/telemetry/vehicle/test-vehicle-id?limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5
    
    def test_get_latest_telemetry(self, client: TestClient, db: Session):
        """Test getting latest telemetry for all vehicles"""
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
        
        # Create telemetry
        telemetry_data_1 = {
            "vehicle_id": "vehicle-1",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed": 45.5,
            "battery_level": 85.0
        }
        telemetry_data_2 = {
            "vehicle_id": "vehicle-2",
            "latitude": 37.7750,
            "longitude": -122.4195,
            "speed": 50.0,
            "battery_level": 90.0
        }
        
        client.post("/api/v1/telemetry", json=telemetry_data_1)
        client.post("/api/v1/telemetry", json=telemetry_data_2)
        
        # Get latest
        response = client.get("/api/v1/telemetry/latest")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert any(item["vehicle_id"] == "vehicle-1" for item in data)
        assert any(item["vehicle_id"] == "vehicle-2" for item in data)
    
    def test_telemetry_pagination(self, client: TestClient, db: Session, sample_vehicle_data):
        """Test telemetry list pagination"""
        # Create vehicle
        vehicle = Vehicle(
            id="test-vehicle-id",
            vin=sample_vehicle_data["vin"],
            make=sample_vehicle_data["make"],
            model=sample_vehicle_data["model"],
            year=sample_vehicle_data["year"],
            status=VehicleStatus.IDLE
        )
        db.add(vehicle)
        db.commit()
        
        # Create multiple telemetry records
        for i in range(10):
            telemetry_data = {
                "vehicle_id": "test-vehicle-id",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "speed": 45.5,
                "battery_level": 85.0
            }
            client.post("/api/v1/telemetry", json=telemetry_data)
        
        # Test pagination
        response = client.get("/api/v1/telemetry?skip=0&limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5
        
        response = client.get("/api/v1/telemetry?skip=5&limit=5")
        assert response.status_code == 200
        assert len(response.json()) == 5


@pytest.mark.database
class TestTelemetryDatabase:
    """Test telemetry database operations"""
    
    def test_telemetry_model_creation(self, db: Session):
        """Test creating telemetry model directly"""
        # Create vehicle first
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
        
        # Create telemetry
        telemetry = Telemetry(
            vehicle_id="test-vehicle-id",
            latitude=37.7749,
            longitude=-122.4194,
            speed=45.5,
            battery_level=85.0,
            odometer=12345.6,
            timestamp=datetime.utcnow()
        )
        
        db.add(telemetry)
        db.commit()
        db.refresh(telemetry)
        
        assert telemetry.id is not None
        assert telemetry.timestamp is not None

# Made with Bob
