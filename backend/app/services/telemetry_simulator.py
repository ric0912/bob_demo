"""
Telemetry data simulator for generating realistic vehicle data
Mimics real-time data streaming from autonomous vehicles
"""
import asyncio
import random
import uuid
from datetime import datetime
from typing import List
import logging

from app.events.event_queue import Event, EventType, event_queue
from app.database import SessionLocal
from app.models.vehicle import Vehicle
from app.models.telemetry import Telemetry

logger = logging.getLogger(__name__)


class TelemetrySimulator:
    """
    Simulates real-time telemetry data generation for active vehicles
    Publishes data to event queue (mimicking Kafka topics)
    """
    
    def __init__(self, interval: float = 5.0):
        """
        Initialize telemetry simulator
        
        Args:
            interval: Seconds between telemetry updates
        """
        self.interval = interval
        self.running = False
        self.task = None
        
        # San Francisco area coordinates for realistic simulation
        self.base_coords = {
            'lat_min': 37.7000,
            'lat_max': 37.8100,
            'lon_min': -122.5200,
            'lon_max': -122.3800
        }
    
    def _generate_telemetry(self, vehicle_id: str, current_data: dict = None) -> dict:
        """
        Generate realistic telemetry data for a vehicle
        
        Args:
            vehicle_id: Vehicle ID
            current_data: Previous telemetry data for continuity
            
        Returns:
            Dictionary with telemetry data
        """
        if current_data:
            # Simulate movement - small changes from previous position
            latitude = current_data['latitude'] + random.uniform(-0.001, 0.001)
            longitude = current_data['longitude'] + random.uniform(-0.001, 0.001)
            speed = max(0, current_data['speed'] + random.uniform(-5, 5))
            battery_level = max(0, current_data['battery_level'] - random.uniform(0.1, 0.5))
            heading = (current_data['heading'] + random.uniform(-10, 10)) % 360
            odometer = current_data['odometer'] + (speed * self.interval / 3600)
        else:
            # Generate initial position
            latitude = random.uniform(self.base_coords['lat_min'], self.base_coords['lat_max'])
            longitude = random.uniform(self.base_coords['lon_min'], self.base_coords['lon_max'])
            speed = random.uniform(0, 60)
            battery_level = random.uniform(60, 100)
            heading = random.uniform(0, 360)
            odometer = random.uniform(1000, 5000)
        
        return {
            'vehicle_id': vehicle_id,
            'latitude': round(latitude, 8),
            'longitude': round(longitude, 8),
            'speed': round(speed, 2),
            'battery_level': round(battery_level, 2),
            'heading': round(heading, 2),
            'odometer': round(odometer, 2),
            'timestamp': datetime.utcnow()
        }
    
    async def _simulate_vehicle_telemetry(self):
        """
        Main simulation loop - generates telemetry for all active vehicles
        """
        logger.info("Telemetry simulator started")
        vehicle_states = {}  # Store last telemetry for each vehicle
        
        while self.running:
            try:
                # Get active vehicles from database
                db = SessionLocal()
                try:
                    active_vehicles = db.query(Vehicle).filter(
                        Vehicle.status.in_(['ACTIVE', 'IDLE'])
                    ).all()
                    
                    for vehicle in active_vehicles:
                        # Get or initialize vehicle state
                        current_state = vehicle_states.get(vehicle.id)
                        
                        # Generate new telemetry
                        telemetry_data = self._generate_telemetry(
                            vehicle.id,
                            current_state
                        )
                        
                        # Store in database
                        telemetry = Telemetry(**telemetry_data)
                        db.add(telemetry)
                        db.commit()
                        
                        # Update vehicle state
                        vehicle_states[vehicle.id] = telemetry_data
                        
                        # Publish event to queue (mimicking Kafka topic)
                        event = Event(
                            event_type=EventType.TELEMETRY_RECEIVED,
                            data=telemetry_data,
                            timestamp=datetime.utcnow(),
                            event_id=str(uuid.uuid4())
                        )
                        await event_queue.publish(event)
                        
                        logger.debug(
                            f"Telemetry generated for {vehicle.vin}: "
                            f"Speed={telemetry_data['speed']}km/h, "
                            f"Battery={telemetry_data['battery_level']}%"
                        )
                    
                    logger.info(f"Generated telemetry for {len(active_vehicles)} vehicles")
                    
                finally:
                    db.close()
                
                # Wait before next update
                await asyncio.sleep(self.interval)
                
            except Exception as e:
                logger.error(f"Error in telemetry simulator: {e}")
                await asyncio.sleep(self.interval)
        
        logger.info("Telemetry simulator stopped")
    
    async def start(self):
        """Start the telemetry simulator"""
        if self.running:
            logger.warning("Telemetry simulator already running")
            return
        
        self.running = True
        self.task = asyncio.create_task(self._simulate_vehicle_telemetry())
        logger.info(f"Telemetry simulator started (interval={self.interval}s)")
    
    async def stop(self):
        """Stop the telemetry simulator"""
        if not self.running:
            logger.warning("Telemetry simulator not running")
            return
        
        self.running = False
        if self.task:
            await self.task
        logger.info("Telemetry simulator stopped")


# Global simulator instance
telemetry_simulator = TelemetrySimulator(interval=5.0)

# Made with Bob