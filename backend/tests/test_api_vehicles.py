"""
Unit tests for Vehicle API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import uuid

from app.models.vehicle import Vehicle, VehicleStatus


@pytest.mark.api
@pytest.mark.unit
class TestVehicleAPI:
    """Test suite for vehicle API endpoints"""
    
    def test_list_vehicles_empty(self, client: TestClient):
        """Test listing vehicles when database is empty"""
        response = client.get("/api/v1/vehicles")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_vehicle_success(self, client: TestClient, sample_vehicle_data):
        """Test successful vehicle creation"""
        response = client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["vin"] == sample_vehicle_data["vin"]
        assert data["make"] == sample_vehicle_data["make"]
        assert data["model"] == sample_vehicle_data["model"]
        assert data["year"] == sample_vehicle_data["year"]
        assert data["status"] == sample_vehicle_data["status"]
        assert "id" in data
        assert "created_at" in data
    
    def test_create_vehicle_duplicate_vin(self, client: TestClient, sample_vehicle_data):
        """Test creating vehicle with duplicate VIN fails"""
        # Create first vehicle
        response1 = client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = client.post("/api/v1/vehicles", json=sample_vehicle_data)
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"].lower()
    
    def test_create_vehicle_invalid_data(self, client: TestClient):
        """Test creating vehicle with invalid data"""
        invalid_data = {
            "vin": "SHORT",  # VIN too short
            "make": "Tesla",
            # Missing required fields
        }
        response = client.post("/api/v1/vehicles", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_get_vehicle_success(self, client: TestClient, sample_vehicle_data):
        """Test retrieving a specific vehicle"""
        # Create vehicle
        create_response = client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = create_response.json()["id"]
        
        # Get vehicle
        response = client.get(f"/api/v1/vehicles/{vehicle_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == vehicle_id
        assert data["vin"] == sample_vehicle_data["vin"]
    
    def test_get_vehicle_not_found(self, client: TestClient):
        """Test retrieving non-existent vehicle"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/vehicles/{fake_id}")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_update_vehicle_success(self, client: TestClient, sample_vehicle_data):
        """Test updating vehicle information"""
        # Create vehicle
        create_response = client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = create_response.json()["id"]
        
        # Update vehicle
        update_data = {"status": "maintenance", "battery_capacity": 80.0}
        response = client.put(f"/api/v1/vehicles/{vehicle_id}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "maintenance"
        assert float(data["battery_capacity"]) == 80.0
    
    def test_update_vehicle_not_found(self, client: TestClient):
        """Test updating non-existent vehicle"""
        fake_id = str(uuid.uuid4())
        update_data = {"status": "maintenance"}
        response = client.put(f"/api/v1/vehicles/{fake_id}", json=update_data)
        assert response.status_code == 404
    
    def test_delete_vehicle_success(self, client: TestClient, sample_vehicle_data):
        """Test deleting a vehicle"""
        # Create vehicle
        create_response = client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = create_response.json()["id"]
        
        # Delete vehicle
        response = client.delete(f"/api/v1/vehicles/{vehicle_id}")
        assert response.status_code == 204
        
        # Verify deletion
        get_response = client.get(f"/api/v1/vehicles/{vehicle_id}")
        assert get_response.status_code == 404
    
    def test_delete_vehicle_not_found(self, client: TestClient):
        """Test deleting non-existent vehicle"""
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/api/v1/vehicles/{fake_id}")
        assert response.status_code == 404
    
    def test_list_vehicles_with_pagination(self, client: TestClient, multiple_vehicles_data):
        """Test listing vehicles with pagination"""
        # Create multiple vehicles
        for vehicle_data in multiple_vehicles_data:
            client.post("/api/v1/vehicles", json=vehicle_data)
        
        # Test pagination
        response = client.get("/api/v1/vehicles?skip=0&limit=3")
        assert response.status_code == 200
        assert len(response.json()) == 3
        
        response = client.get("/api/v1/vehicles?skip=3&limit=3")
        assert response.status_code == 200
        assert len(response.json()) == 2  # Only 2 remaining
    
    def test_get_vehicle_status(self, client: TestClient, sample_vehicle_data):
        """Test getting vehicle status endpoint"""
        # Create vehicle
        create_response = client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = create_response.json()["id"]
        
        # Get status
        response = client.get(f"/api/v1/vehicles/{vehicle_id}/status")
        assert response.status_code == 200
        
        data = response.json()
        assert data["vehicle_id"] == vehicle_id
        assert data["status"] == sample_vehicle_data["status"]
        assert "battery_capacity" in data
        assert "last_updated" in data
    
    def test_vehicle_status_change_event(self, client: TestClient, sample_vehicle_data):
        """Test that status change triggers event"""
        # Create vehicle
        create_response = client.post("/api/v1/vehicles", json=sample_vehicle_data)
        vehicle_id = create_response.json()["id"]
        
        # Update status
        update_data = {"status": "active"}
        response = client.put(f"/api/v1/vehicles/{vehicle_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["status"] == "active"


@pytest.mark.api
@pytest.mark.database
class TestVehicleDatabase:
    """Test vehicle database operations"""
    
    def test_vehicle_model_creation(self, db: Session):
        """Test creating vehicle model directly"""
        vehicle = Vehicle(
            id=str(uuid.uuid4()),
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            license_plate="ABC123",
            status=VehicleStatus.IDLE,
            battery_capacity=75.5
        )
        
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        
        assert vehicle.id is not None
        assert vehicle.created_at is not None
        assert vehicle.updated_at is not None
    
    def test_vehicle_unique_vin_constraint(self, db: Session):
        """Test VIN uniqueness constraint"""
        vehicle1 = Vehicle(
            id=str(uuid.uuid4()),
            vin="1HGBH41JXMN109186",
            make="Tesla",
            model="Model 3",
            year=2023,
            status=VehicleStatus.IDLE
        )
        
        vehicle2 = Vehicle(
            id=str(uuid.uuid4()),
            vin="1HGBH41JXMN109186",  # Same VIN
            make="Tesla",
            model="Model Y",
            year=2023,
            status=VehicleStatus.IDLE
        )
        
        db.add(vehicle1)
        db.commit()
        
        db.add(vehicle2)
        with pytest.raises(Exception):  # Should raise integrity error
            db.commit()

# Made with Bob
