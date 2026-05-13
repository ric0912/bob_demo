"""
Events package for event-driven architecture
"""
from app.events.event_queue import EventQueue, Event, EventType, event_queue
from app.events.event_handlers import register_event_handlers

__all__ = [
    "EventQueue",
    "Event",
    "EventType",
    "event_queue",
    "register_event_handlers"
]

# Made with Bob
