"""
Integration tests for complete workflows
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime
import time


@pytest.mark.integration
@pytest.mark.slow
class TestVehicleLifecycleWorkflow:
    """Test complete vehicle lifecycle from registration to decommission"""
    
    def test_complete_vehicle_lifecycle(self, client: TestClient):
        """Test full vehicle lifecycle workflow"""
        # 1. Register new vehicle
        vehicle_data = {
            "vin": "1HGBH41JXMN109186",
            "make": "Tesla",
            "model": "Model 3",
            "year": 2023,
            "license_plate": "ABC123",
            "status": "idle",
            "battery_capacity": 75.5
        }
        create_response = client.post("/api/v1/vehicles", json=vehicle_data)
        assert create_response.status_code == 201
        vehicle_id = create_response.json()["id"]
        
        # 2. Submit initial telemetry
        telemetry_data = {
            "vehicle_id": vehicle_id,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed": 0.0,
            "battery_level": 100.0,
            "odometer": 0.0
        }
        telemetry_response = client.post("/api/v1/telemetry", json=telemetry_data)
        assert telemetry_response.status_code == 201
        
        # 3. Create fleet assignment
        assignment_data = {
            "vehicle_id": vehicle_id,
            "route_id": "route-123",
            "driver_id": "driver-456",
            "status": "assigned"
        }
        assignment_response = client.post("/api/v1/fleet/assignments", json=assignment_data)
        assert assignment_response.status_code == 201
        assignment_id = assignment_response.json()["id"]
        
        # 4. Verify vehicle status changed to active
        vehicle_response = client.get(f"/api/v1/vehicles/{vehicle_id}")
        assert vehicle_response.json()["status"] == "active"
        
        # 5. Update assignment to in_progress
        update_assignment = {"status": "in_progress"}
        client.put(f"/api/v1/fleet/assignments/{assignment_id}", json=update_assignment)
        
        # 6. Submit telemetry during journey
        for i in range(3):
            journey_telemetry = {
                "vehicle_id": vehicle_id,
                "latitude": 37.7749 + i * 0.01,
                "longitude": -122.4194 + i * 0.01,
                "speed": 45.5,
                "battery_level": 100.0 - i * 5,
                "odometer": i * 10.0
            }
            client.post("/api/v1/telemetry", json=journey_telemetry)
        
        # 7. Complete assignment
        complete_assignment = {"status": "completed"}
        complete_response = client.put(
            f"/api/v1/fleet/assignments/{assignment_id}",
            json=complete_assignment
        )
        assert complete_response.status_code == 200
        
        # 8. Verify vehicle returned to idle
        final_vehicle = client.get(f"/api/v1/vehicles/{vehicle_id}")
        assert final_vehicle.json()["status"] == "idle"
        
        # 9. Check analytics
        analytics_response = client.get(f"/api/v1/analytics/vehicle/{vehicle_id}")
        assert analytics_response.status_code == 200
        analytics = analytics_response.json()
        assert analytics["telemetry_records"] >= 4
        assert analytics["assignments_completed"] >= 1
        
        # 10. Delete vehicle
        delete_response = client.delete(f"/api/v1/vehicles/{vehicle_id}")
        assert delete_response.status_code == 204


@pytest.mark.integration
class TestFleetOperationsWorkflow:
    """Test fleet management operations workflow"""
    
    def test_multi_vehicle_fleet_operations(self, client: TestClient):
        """Test managing multiple vehicles in fleet"""
        vehicle_ids = []
        
        # Create multiple vehicles
        for i in range(3):
            vehicle_data = {
                "vin": f"1HGBH41JXMN10918{i}",
                "make": "Tesla",
                "model": f"Model {chr(51+i)}",  # Model 3, 4, 5
                "year": 2023,
                "license_plate": f"ABC{i:03d}",
                "status": "idle",
                "battery_capacity": 75.5
            }
            response = client.post("/api/v1/vehicles", json=vehicle_data)
            assert response.status_code == 201
            vehicle_ids.append(response.json()["id"])
        
        # Check fleet overview
        overview_response = client.get("/api/v1/fleet/overview")
        assert overview_response.status_code == 200
        overview = overview_response.json()
        assert overview["total_vehicles"] == 3
        
        # Assign all vehicles
        assignment_ids = []
        for i, vehicle_id in enumerate(vehicle_ids):
            assignment_data = {
                "vehicle_id": vehicle_id,
                "route_id": f"route-{i}",
                "driver_id": f"driver-{i}",
                "status": "assigned"
            }
            response = client.post("/api/v1/fleet/assignments", json=assignment_data)
            assert response.status_code == 201
            assignment_ids.append(response.json()["id"])
        
        # Verify all assignments active
        overview_response = client.get("/api/v1/fleet/overview")
        overview = overview_response.json()
        assert overview["active_assignments"] == 3
        
        # Complete all assignments
        for assignment_id in assignment_ids:
            update_data = {"status": "completed"}
            response = client.put(f"/api/v1/fleet/assignments/{assignment_id}", json=update_data)
            assert response.status_code == 200
        
        # Verify no active assignments
        overview_response = client.get("/api/v1/fleet/overview")
        overview = overview_response.json()
        assert overview["active_assignments"] == 0


@pytest.mark.integration
class TestTelemetryStreamingWorkflow:
    """Test real-time telemetry streaming workflow"""
    
    def test_continuous_telemetry_submission(self, client: TestClient):
        """Test continuous telemetry data submission"""
        # Create vehicle
        vehicle_data = {
            "vin": "1HGBH41JXMN109186",
            "make": "Tesla",
            "model": "Model 3",
            "year": 2023,
            "status": "active",
            "battery_capacity": 75.5
        }
        vehicle_response = client.post("/api/v1/vehicles", json=vehicle_data)
        vehicle_id = vehicle_response.json()["id"]
        
        # Submit telemetry stream
        telemetry_count = 10
        for i in range(telemetry_count):
            telemetry_data = {
                "vehicle_id": vehicle_id,
                "latitude": 37.7749 + i * 0.001,
                "longitude": -122.4194 + i * 0.001,
                "speed": 45.5 + i * 0.5,
                "battery_level": 100.0 - i * 1.0,
                "odometer": i * 5.0
            }
            response = client.post("/api/v1/telemetry", json=telemetry_data)
            assert response.status_code == 201
        
        # Verify all telemetry recorded
        telemetry_response = client.get(f"/api/v1/telemetry/vehicle/{vehicle_id}")
        assert len(telemetry_response.json()) == telemetry_count
        
        # Check latest telemetry
        latest_response = client.get("/api/v1/telemetry/latest")
        assert latest_response.status_code == 200
        latest_data = latest_response.json()
        assert len(latest_data) >= 1
        vehicle_telemetry = next(
            (item for item in latest_data if item["vehicle_id"] == vehicle_id),
            None
        )
        assert vehicle_telemetry is not None


@pytest.mark.integration
class TestAlertManagementWorkflow:
    """Test alert generation and management workflow"""
    
    def test_alert_lifecycle(self, client: TestClient, db: Session):
        """Test complete alert lifecycle"""
        from app.models.vehicle import Vehicle, VehicleStatus
        from app.models.alert import Alert, AlertSeverity
        
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
        
        # Create multiple alerts
        alert_ids = []
        severities = [AlertSeverity.INFO, AlertSeverity.WARNING, AlertSeverity.CRITICAL]
        for i, severity in enumerate(severities):
            alert = Alert(
                id=f"alert-{i}",
                vehicle_id="test-vehicle-id",
                alert_type=f"alert_type_{i}",
                severity=severity,
                message=f"Alert message {i}",
                acknowledged=False
            )
            db.add(alert)
            alert_ids.append(alert.id)
        db.commit()
        
        # List unacknowledged alerts
        alerts_response = client.get("/api/v1/fleet/alerts?acknowledged=false")
        assert alerts_response.status_code == 200
        alerts = alerts_response.json()
        assert len(alerts) == 3
        
        # Acknowledge alerts one by one
        for alert_id in alert_ids:
            ack_response = client.post(f"/api/v1/fleet/alerts/{alert_id}/acknowledge")
            assert ack_response.status_code == 200
        
        # Verify all acknowledged
        alerts_response = client.get("/api/v1/fleet/alerts?acknowledged=false")
        assert len(alerts_response.json()) == 0


@pytest.mark.integration
class TestAnalyticsReportingWorkflow:
    """Test analytics and reporting workflow"""
    
    def test_comprehensive_analytics_reporting(self, client: TestClient):
        """Test generating comprehensive analytics reports"""
        # Create vehicles
        vehicle_ids = []
        for i in range(2):
            vehicle_data = {
                "vin": f"1HGBH41JXMN10918{i}",
                "make": "Tesla",
                "model": "Model 3",
                "year": 2023,
                "status": "idle",
                "battery_capacity": 75.5
            }
            response = client.post("/api/v1/vehicles", json=vehicle_data)
            vehicle_ids.append(response.json()["id"])
        
        # Generate telemetry for both vehicles
        for vehicle_id in vehicle_ids:
            for i in range(5):
                telemetry_data = {
                    "vehicle_id": vehicle_id,
                    "latitude": 37.7749,
                    "longitude": -122.4194,
                    "speed": 45.5,
                    "battery_level": 85.0,
                    "odometer": i * 10.0
                }
                client.post("/api/v1/telemetry", json=telemetry_data)
        
        # Get summary analytics
        summary_response = client.get("/api/v1/analytics/summary")
        assert summary_response.status_code == 200
        summary = summary_response.json()
        assert summary["total_vehicles"] == 2
        assert summary["total_telemetry_records"] >= 10
        
        # Get performance metrics
        performance_response = client.get("/api/v1/analytics/performance")
        assert performance_response.status_code == 200
        
        # Get trends
        trends_response = client.get("/api/v1/analytics/trends?days=7")
        assert trends_response.status_code == 200
        trends = trends_response.json()
        assert "telemetry_trend" in trends
        assert "assignments_trend" in trends
        assert "alerts_trend" in trends
        
        # Get individual vehicle analytics
        for vehicle_id in vehicle_ids:
            vehicle_analytics = client.get(f"/api/v1/analytics/vehicle/{vehicle_id}")
            assert vehicle_analytics.status_code == 200
            assert vehicle_analytics.json()["telemetry_records"] >= 5


@pytest.mark.integration
class TestErrorHandlingWorkflow:
    """Test error handling in workflows"""
    
    def test_invalid_assignment_workflow(self, client: TestClient):
        """Test handling invalid assignment scenarios"""
        # Try to create assignment for non-existent vehicle
        assignment_data = {
            "vehicle_id": "non-existent-id",
            "route_id": "route-123",
            "driver_id": "driver-456",
            "status": "assigned"
        }
        response = client.post("/api/v1/fleet/assignments", json=assignment_data)
        assert response.status_code == 404
    
    def test_duplicate_vehicle_workflow(self, client: TestClient):
        """Test handling duplicate vehicle registration"""
        vehicle_data = {
            "vin": "1HGBH41JXMN109186",
            "make": "Tesla",
            "model": "Model 3",
            "year": 2023,
            "status": "idle",
            "battery_capacity": 75.5
        }
        
        # Create first vehicle
        response1 = client.post("/api/v1/vehicles", json=vehicle_data)
        assert response1.status_code == 201
        
        # Try to create duplicate
        response2 = client.post("/api/v1/vehicles", json=vehicle_data)
        assert response2.status_code == 400
    
    def test_telemetry_for_nonexistent_vehicle(self, client: TestClient):
        """Test submitting telemetry for non-existent vehicle"""
        telemetry_data = {
            "vehicle_id": "non-existent-id",
            "latitude": 37.7749,
            "longitude": -122.4194,
            "speed": 45.5,
            "battery_level": 85.0
        }
        response = client.post("/api/v1/telemetry", json=telemetry_data)
        assert response.status_code == 404


@pytest.mark.integration
class TestHealthCheckWorkflow:
    """Test health check and system status workflow"""
    
    def test_health_endpoints(self, client: TestClient):
        """Test all health check endpoints"""
        # Health check
        health_response = client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "healthy"
        
        # Readiness check
        ready_response = client.get("/ready")
        assert ready_response.status_code == 200
        assert ready_response.json()["status"] == "ready"
        
        # Liveness check
        live_response = client.get("/live")
        assert live_response.status_code == 200
        assert live_response.json()["status"] == "alive"
        
        # System status
        status_response = client.get("/api/v1/status")
        assert status_response.status_code == 200
        assert "application" in status_response.json()
        assert "event_queue" in status_response.json()

# Made with Bob
