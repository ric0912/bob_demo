"""
WebSocket endpoints for real-time data streaming
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Set
import asyncio
import json
import logging
from datetime import datetime

from app.events.event_queue import Event, EventType, event_queue

logger = logging.getLogger(__name__)

router = APIRouter()


class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.event_listener_task = None
    
    async def connect(self, websocket: WebSocket):
        """Accept and register a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending to WebSocket: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def listen_to_events(self):
        """Listen to event queue and broadcast to WebSocket clients"""
        logger.info("WebSocket event listener started")
        
        async def telemetry_handler(event: Event):
            """Handle telemetry events and broadcast to clients"""
            # Convert datetime objects to ISO format strings
            data = event.data.copy()
            if 'timestamp' in data and hasattr(data['timestamp'], 'isoformat'):
                data['timestamp'] = data['timestamp'].isoformat()
            
            message = {
                'type': 'telemetry',
                'event_id': event.event_id,
                'timestamp': event.timestamp.isoformat(),
                'data': data
            }
            await self.broadcast(message)
        
        async def alert_handler(event: Event):
            """Handle alert events and broadcast to clients"""
            message = {
                'type': 'alert',
                'event_id': event.event_id,
                'timestamp': event.timestamp.isoformat(),
                'data': event.data
            }
            await self.broadcast(message)
        
        async def vehicle_status_handler(event: Event):
            """Handle vehicle status change events"""
            message = {
                'type': 'vehicle_status',
                'event_id': event.event_id,
                'timestamp': event.timestamp.isoformat(),
                'data': event.data
            }
            await self.broadcast(message)
        
        # Subscribe to events
        event_queue.subscribe(EventType.TELEMETRY_RECEIVED, telemetry_handler)
        event_queue.subscribe(EventType.ALERT_CREATED, alert_handler)
        event_queue.subscribe(EventType.VEHICLE_STATUS_CHANGED, vehicle_status_handler)
        
        logger.info("WebSocket subscribed to event queue")


# Global connection manager
manager = ConnectionManager()


@router.websocket("/ws/telemetry")
async def websocket_telemetry(websocket: WebSocket):
    """
    WebSocket endpoint for real-time telemetry streaming
    
    Clients connect to this endpoint to receive:
    - Real-time telemetry data from all vehicles
    - Alert notifications
    - Vehicle status changes
    """
    await manager.connect(websocket)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            'type': 'connection',
            'status': 'connected',
            'timestamp': datetime.utcnow().isoformat(),
            'message': 'Connected to telemetry stream'
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for messages from client (ping/pong, subscriptions, etc.)
                data = await websocket.receive_text()
                
                # Echo back for ping/pong
                if data == 'ping':
                    await websocket.send_json({
                        'type': 'pong',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"Error in WebSocket loop: {e}")
                break
    
    finally:
        manager.disconnect(websocket)


@router.get("/ws/stats")
async def websocket_stats():
    """Get WebSocket connection statistics"""
    return {
        'active_connections': len(manager.active_connections),
        'event_queue_stats': event_queue.get_stats()
    }


# Made with Bob