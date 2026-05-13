"""
Event handlers for processing events from the queue
"""
import logging
from app.events.event_queue import Event, EventType

logger = logging.getLogger(__name__)


async def handle_vehicle_registered(event: Event) -> None:
    """
    Handle vehicle registration event
    
    Args:
        event: Vehicle registration event
    """
    vehicle_data = event.data
    logger.info(f"Vehicle registered: {vehicle_data.get('vin')} - {vehicle_data.get('id')}")
    # Additional processing can be added here
    # e.g., send notification, update cache, trigger workflows


async def handle_vehicle_status_changed(event: Event) -> None:
    """
    Handle vehicle status change event
    
    Args:
        event: Vehicle status change event
    """
    vehicle_id = event.data.get('vehicle_id')
    old_status = event.data.get('old_status')
    new_status = event.data.get('new_status')
    logger.info(f"Vehicle {vehicle_id} status changed: {old_status} -> {new_status}")
    # Additional processing can be added here


async def handle_telemetry_received(event: Event) -> None:
    """
    Handle telemetry data received event
    
    Args:
        event: Telemetry received event
    """
    vehicle_id = event.data.get('vehicle_id')
    battery_level = event.data.get('battery_level')
    
    # Check for low battery and create alert if needed
    if battery_level and battery_level < 20:
        logger.warning(f"Low battery detected for vehicle {vehicle_id}: {battery_level}%")
        # Could trigger alert creation here
    
    logger.debug(f"Telemetry processed for vehicle {vehicle_id}")


async def handle_alert_created(event: Event) -> None:
    """
    Handle alert creation event
    
    Args:
        event: Alert created event
    """
    alert_data = event.data
    severity = alert_data.get('severity')
    alert_type = alert_data.get('alert_type')
    vehicle_id = alert_data.get('vehicle_id')
    
    logger.warning(f"Alert created: {alert_type} ({severity}) for vehicle {vehicle_id}")
    
    # Send notifications based on severity
    if severity == 'critical':
        logger.critical(f"CRITICAL ALERT: {alert_type} for vehicle {vehicle_id}")
        # Could send SMS, email, or push notification here


async def handle_assignment_created(event: Event) -> None:
    """
    Handle fleet assignment creation event
    
    Args:
        event: Assignment created event
    """
    assignment_data = event.data
    vehicle_id = assignment_data.get('vehicle_id')
    route_id = assignment_data.get('route_id')
    
    logger.info(f"Assignment created: Vehicle {vehicle_id} assigned to route {route_id}")
    # Additional processing can be added here


async def handle_assignment_completed(event: Event) -> None:
    """
    Handle fleet assignment completion event
    
    Args:
        event: Assignment completed event
    """
    assignment_data = event.data
    vehicle_id = assignment_data.get('vehicle_id')
    assignment_id = assignment_data.get('assignment_id')
    
    logger.info(f"Assignment {assignment_id} completed for vehicle {vehicle_id}")
    # Additional processing can be added here


def register_event_handlers(event_queue) -> None:
    """
    Register all event handlers with the event queue
    
    Args:
        event_queue: EventQueue instance
    """
    event_queue.subscribe(EventType.VEHICLE_REGISTERED, handle_vehicle_registered)
    event_queue.subscribe(EventType.VEHICLE_STATUS_CHANGED, handle_vehicle_status_changed)
    event_queue.subscribe(EventType.TELEMETRY_RECEIVED, handle_telemetry_received)
    event_queue.subscribe(EventType.ALERT_CREATED, handle_alert_created)
    event_queue.subscribe(EventType.ASSIGNMENT_CREATED, handle_assignment_created)
    event_queue.subscribe(EventType.ASSIGNMENT_COMPLETED, handle_assignment_completed)
    
    logger.info("All event handlers registered")

# Made with Bob
