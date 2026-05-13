"""
Pytest configuration and fixtures for testing
"""
import pytest
import asyncio
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.config import settings

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create test session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test
    """
    # Create tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database dependency override
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for async tests
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_vehicle_data():
    """
    Sample vehicle data for testing
    """
    return {
        "vin": "1HGBH41JXMN109186",
        "make": "Tesla",
        "model": "Model 3",
        "year": 2023,
        "license_plate": "ABC123",
        "status": "idle",
        "battery_capacity": 75.5
    }


@pytest.fixture
def sample_telemetry_data():
    """
    Sample telemetry data for testing
    """
    return {
        "vehicle_id": "test-vehicle-id",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "speed": 45.5,
        "battery_level": 85.0,
        "odometer": 12345.6,
        "fuel_level": None
    }


@pytest.fixture
def sample_fleet_assignment_data():
    """
    Sample fleet assignment data for testing
    """
    return {
        "vehicle_id": "test-vehicle-id",
        "route_id": "route-123",
        "driver_id": "driver-456",
        "status": "assigned"
    }


@pytest.fixture
def multiple_vehicles_data():
    """
    Multiple vehicles for testing list operations
    """
    return [
        {
            "vin": f"1HGBH41JXMN10918{i}",
            "make": "Tesla",
            "model": "Model 3",
            "year": 2023,
            "license_plate": f"ABC{i:03d}",
            "status": "idle",
            "battery_capacity": 75.5
        }
        for i in range(5)
    ]

# Made with Bob
