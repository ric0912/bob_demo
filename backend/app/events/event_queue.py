"""
In-memory event queue implementation using asyncio
"""
import asyncio
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Event type enumeration"""
    VEHICLE_REGISTERED = "vehicle_registered"
    VEHICLE_STATUS_CHANGED = "vehicle_status_changed"
    TELEMETRY_RECEIVED = "telemetry_received"
    ALERT_CREATED = "alert_created"
    ASSIGNMENT_CREATED = "assignment_created"
    ASSIGNMENT_COMPLETED = "assignment_completed"


@dataclass
class Event:
    """Event data structure"""
    event_type: EventType
    data: Dict[str, Any]
    timestamp: datetime
    event_id: str


class EventQueue:
    """
    In-memory event queue for pub/sub messaging
    Provides asynchronous event publishing and subscription
    """
    
    def __init__(self, max_size: int = 1000):
        """
        Initialize event queue
        
        Args:
            max_size: Maximum queue size
        """
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._subscribers: Dict[EventType, List[Callable]] = {}
        self._running = False
        self._processor_task = None
        logger.info(f"EventQueue initialized with max_size={max_size}")
    
    async def publish(self, event: Event) -> None:
        """
        Publish an event to the queue
        
        Args:
            event: Event to publish
        """
        try:
            await self._queue.put(event)
            logger.debug(f"Event published: {event.event_type} - {event.event_id}")
        except asyncio.QueueFull:
            logger.error(f"Queue full, dropping event: {event.event_type}")
    
    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """
        Subscribe to an event type
        
        Args:
            event_type: Type of event to subscribe to
            handler: Async function to handle the event
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info(f"Handler subscribed to {event_type}")
    
    def unsubscribe(self, event_type: EventType, handler: Callable) -> None:
        """
        Unsubscribe from an event type
        
        Args:
            event_type: Type of event to unsubscribe from
            handler: Handler function to remove
        """
        if event_type in self._subscribers:
            try:
                self._subscribers[event_type].remove(handler)
                logger.info(f"Handler unsubscribed from {event_type}")
            except ValueError:
                logger.warning(f"Handler not found for {event_type}")
    
    async def _process_events(self) -> None:
        """
        Process events from the queue
        Runs continuously while the queue is active
        """
        logger.info("Event processor started")
        while self._running:
            try:
                # Wait for event with timeout
                event = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=1.0
                )
                
                # Get subscribers for this event type
                handlers = self._subscribers.get(event.event_type, [])
                
                if not handlers:
                    logger.debug(f"No handlers for event type: {event.event_type}")
                    continue
                
                # Execute all handlers concurrently
                tasks = [handler(event) for handler in handlers]
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Log any errors
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        logger.error(
                            f"Handler {i} failed for {event.event_type}: {result}"
                        )
                
                logger.debug(f"Event processed: {event.event_type} - {event.event_id}")
                
            except asyncio.TimeoutError:
                # No events in queue, continue waiting
                continue
            except Exception as e:
                logger.error(f"Error processing event: {e}")
        
        logger.info("Event processor stopped")
    
    async def start(self) -> None:
        """Start the event processor"""
        if self._running:
            logger.warning("Event processor already running")
            return
        
        self._running = True
        self._processor_task = asyncio.create_task(self._process_events())
        logger.info("Event queue started")
    
    async def stop(self) -> None:
        """Stop the event processor"""
        if not self._running:
            logger.warning("Event processor not running")
            return
        
        self._running = False
        if self._processor_task:
            await self._processor_task
        logger.info("Event queue stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get queue statistics
        
        Returns:
            Dictionary with queue stats
        """
        return {
            "queue_size": self._queue.qsize(),
            "max_size": self._queue.maxsize,
            "running": self._running,
            "subscriber_count": sum(len(handlers) for handlers in self._subscribers.values()),
            "event_types": list(self._subscribers.keys())
        }


# Global event queue instance
event_queue = EventQueue()

# Made with Bob
