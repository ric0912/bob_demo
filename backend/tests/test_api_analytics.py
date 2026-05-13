"""
Unit tests for Analytics API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from app.models.vehicle import Vehicle, VehicleStatus
from app.models.telemetry import Telemetry
from app.models.fleet import FleetAssignment, AssignmentStatus
from app.models.alert import Alert, AlertSeverity


@pytest.mark.api
@pytest.mark.unit
class TestAnalyticsAPI:
    """Test suite for analytics API endpoints"""
    
    def test_get_analytics_summary_empty(self, client: TestClient):
        """Test analytics summary with empty database"""
        response = client.get("/api/v1/analytics/summary")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_vehicles"] == 0
        assert data["active_vehicles"] == 0
        assert data["total_telemetry_records"] == 0
    
    def test_get_analytics_summary_with_data(self, client: TestClient, db: Session):
        """Test analytics summary with data"""
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
        telemetry = Telemetry(
            vehicle_id="vehicle-1",
            latitude=37.7749,
            longitude=-122.4194,
            speed=45.5,
            battery_level=85.0,
            timestamp=datetime.utcnow()
        )
        db.add(telemetry)
        db.commit()
        
        # Get summary
        response = client.get("/api/v1/analytics/summary")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_vehicles"] == 2
        assert data["active_vehicles"] == 1
        assert data["total_telemetry_records"] == 1
    
    def test_get_vehicle_analytics_not_found(self, client: TestClient):
        """Test getting analytics for non-existent vehicle"""
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/analytics/vehicle/{fake_id}")
        assert response.status_code == 404
    
    def test_get_vehicle_analytics_success(self, client: TestClient, db: Session):
        """Test getting analytics for specific vehicle"""
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
        
        # Create telemetry records
        for i in range(5):
            telemetry = Telemetry(
                vehicle_id="test-vehicle-id",
                latitude=37.7749,
                longitude=-122.4194,
                speed=45.5 + i,
                battery_level=85.0,
                odometer=1000.0 + i * 10,
                timestamp=datetime.utcnow() - timedelta(days=i)
            )
            db.add(telemetry)
        db.commit()
        
        # Get analytics
        response = client.get("/api/v1/analytics/vehicle/test-vehicle-id?days=7")
        assert response.status_code == 200
        
        data = response.json()
        assert data["vehicle_id"] == "test-vehicle-id"
        assert data["vin"] == "1HGBH41JXMN109186"
        assert data["period_days"] == 7
        assert data["telemetry_records"] == 5
        assert data["average_speed"] is not None
    
    def test_get_vehicle_analytics_with_assignments(self, client: TestClient, db: Session):
        """Test vehicle analytics includes assignment data"""
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
        
        # Create completed assignment
        assignment = FleetAssignment(
            id=str(uuid.uuid4()),
            vehicle_id="test-vehicle-id",
            route_id="route-123",
            driver_id="driver-456",
            status=AssignmentStatus.COMPLETED,
            completed_at=datetime.utcnow()
        )
        db.add(assignment)
        db.commit()
        
        # Get analytics
        response = client.get("/api/v1/analytics/vehicle/test-vehicle-id?days=7")
        assert response.status_code == 200
        
        data = response.json()
        assert data["assignments_completed"] == 1
    
    def test_get_performance_metrics(self, client: TestClient, db: Session):
        """Test getting fleet performance metrics"""
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
        
        # Get performance metrics
        response = client.get("/api/v1/analytics/performance?days=7")
        assert response.status_code == 200
        
        data = response.json()
        assert data["period_days"] == 7
        assert "vehicle_utilization_rate" in data
        assert "alerts_per_day" in data
    
    def test_get_performance_metrics_with_assignments(self, client: TestClient, db: Session):
        """Test performance metrics with completed assignments"""
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
        
        # Create completed assignment
        now = datetime.utcnow()
        assignment = FleetAssignment(
            id=str(uuid.uuid4()),
            vehicle_id="test-vehicle-id",
            route_id="route-123",
            driver_id="driver-456",
            status=AssignmentStatus.COMPLETED,
            assigned_at=now - timedelta(hours=2),
            completed_at=now
        )
        db.add(assignment)
        db.commit()
        
        # Get performance metrics
        response = client.get("/api/v1/analytics/performance?days=7")
        assert response.status_code == 200
        
        data = response.json()
        assert "avg_assignment_completion_seconds" in data
    
    def test_get_trends_empty(self, client: TestClient):
        """Test getting trends with empty database"""
        response = client.get("/api/v1/analytics/trends?days=7")
        assert response.status_code == 200
        
        data = response.json()
        assert data["period_days"] == 7
        assert "telemetry_trend" in data
        assert "assignments_trend" in data
        assert "alerts_trend" in data
    
    def test_get_trends_with_data(self, client: TestClient, db: Session):
        """Test getting trends with historical data"""
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
        
        # Create telemetry over multiple days
        for i in range(5):
            telemetry = Telemetry(
                vehicle_id="test-vehicle-id",
                latitude=37.7749,
                longitude=-122.4194,
                speed=45.5,
                battery_level=85.0,
                timestamp=datetime.utcnow() - timedelta(days=i)
            )
            db.add(telemetry)
        
        # Create assignments over multiple days
        for i in range(3):
            assignment = FleetAssignment(
                id=str(uuid.uuid4()),
                vehicle_id="test-vehicle-id",
                route_id=f"route-{i}",
                driver_id=f"driver-{i}",
                status=AssignmentStatus.COMPLETED,
                assigned_at=datetime.utcnow() - timedelta(days=i),
                completed_at=datetime.utcnow() - timedelta(days=i, hours=-2)
            )
            db.add(assignment)
        
        db.commit()
        
        # Get trends
        response = client.get("/api/v1/analytics/trends?days=7")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["telemetry_trend"]) > 0
        assert len(data["assignments_trend"]) > 0
    
    def test_analytics_summary_with_critical_alerts(self, client: TestClient, db: Session):
        """Test analytics summary includes critical alerts"""
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
        
        # Create critical alert
        alert = Alert(
            id=str(uuid.uuid4()),
            vehicle_id="test-vehicle-id",
            alert_type="critical_failure",
            severity=AlertSeverity.CRITICAL,
            message="Critical system failure",
            acknowledged=False
        )
        db.add(alert)
        db.commit()
        
        # Get summary
        response = client.get("/api/v1/analytics/summary")
        assert response.status_code == 200
        
        data = response.json()
        assert data["critical_alerts"] == 1
    
    def test_analytics_summary_average_battery(self, client: TestClient, db: Session):
        """Test analytics summary calculates average battery level"""
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
        
        # Create telemetry with different battery levels
        battery_levels = [80.0, 85.0, 90.0]
        for level in battery_levels:
            telemetry = Telemetry(
                vehicle_id="test-vehicle-id",
                latitude=37.7749,
                longitude=-122.4194,
                speed=45.5,
                battery_level=level,
                timestamp=datetime.utcnow()
            )
            db.add(telemetry)
        db.commit()
        
        # Get summary
        response = client.get("/api/v1/analytics/summary")
        assert response.status_code == 200
        
        data = response.json()
        assert data["average_battery_level"] is not None
        assert 80.0 <= data["average_battery_level"] <= 90.0
    
    def test_vehicle_analytics_custom_period(self, client: TestClient, db: Session):
        """Test vehicle analytics with custom time period"""
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
        
        # Create telemetry
        telemetry = Telemetry(
            vehicle_id="test-vehicle-id",
            latitude=37.7749,
            longitude=-122.4194,
            speed=45.5,
            battery_level=85.0,
            timestamp=datetime.utcnow()
        )
        db.add(telemetry)
        db.commit()
        
        # Test different periods
        for days in [1, 7, 30]:
            response = client.get(f"/api/v1/analytics/vehicle/test-vehicle-id?days={days}")
            assert response.status_code == 200
            assert response.json()["period_days"] == days


@pytest.mark.integration
class TestAnalyticsIntegration:
    """Integration tests for analytics workflows"""
    
    def test_complete_analytics_workflow(self, client: TestClient, db: Session):
        """Test complete analytics workflow from vehicle creation to reporting"""
        # Create vehicle
        vehicle_data = {
            "vin": "1HGBH41JXMN109186",
            "make": "Tesla",
            "model": "Model 3",
            "year": 2023,
            "license_plate": "ABC123",
            "status": "idle",
            "battery_capacity": 75.5
        }
        vehicle_response = client.post("/api/v1/vehicles", json=vehicle_data)
        assert vehicle_response.status_code == 201
        vehicle_id = vehicle_response.json()["id"]
        
        # Create telemetry
        telemetry_data = {
            "vehicle_id": vehicle_id,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed": 45.5,
            "battery_level": 85.0,
            "odometer": 12345.6
        }
        telemetry_response = client.post("/api/v1/telemetry", json=telemetry_data)
        assert telemetry_response.status_code == 201
        
        # Get analytics
        analytics_response = client.get(f"/api/v1/analytics/vehicle/{vehicle_id}")
        assert analytics_response.status_code == 200
        
        analytics_data = analytics_response.json()
        assert analytics_data["vehicle_id"] == vehicle_id
        assert analytics_data["telemetry_records"] >= 1

# Made with Bob
