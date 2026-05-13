# Pub/Sub Architecture - Mimicking Confluent Kafka Topics

## Overview

This Fleet Management Platform implements an **in-memory event-driven architecture** that mimics Confluent Kafka's pub/sub messaging pattern. Instead of using actual Kafka, we've built a lightweight, asynchronous event queue system using Python's `asyncio` that demonstrates the same concepts.

## Architecture Components

### 1. Event Queue System (`backend/app/events/event_queue.py`)

**Mimics**: Kafka Topics and Brokers

The `EventQueue` class provides:
- **Asynchronous message queue** using `asyncio.Queue`
- **Pub/Sub pattern** with topic-based routing
- **Event types** (similar to Kafka topics):
  - `VEHICLE_REGISTERED`
  - `VEHICLE_STATUS_CHANGED`
  - `TELEMETRY_RECEIVED` ← Main telemetry stream
  - `ALERT_CREATED`
  - `ASSIGNMENT_CREATED`
  - `ASSIGNMENT_COMPLETED`

```python
# Publishing an event (like Kafka Producer)
event = Event(
    event_type=EventType.TELEMETRY_RECEIVED,
    data=telemetry_data,
    timestamp=datetime.utcnow(),
    event_id=str(uuid.uuid4())
)
await event_queue.publish(event)

# Subscribing to events (like Kafka Consumer)
event_queue.subscribe(EventType.TELEMETRY_RECEIVED, handler_function)
```

### 2. Event Handlers (`backend/app/events/event_handlers.py`)

**Mimics**: Kafka Consumers

Event handlers are async functions that process events from specific topics:
- `handle_telemetry_received()` - Processes telemetry data
- `handle_alert_created()` - Handles alert notifications
- `handle_vehicle_status_changed()` - Tracks vehicle state changes

Each handler can:
- Process data
- Trigger side effects (notifications, logging)
- Create new events (event chaining)

### 3. Telemetry Simulator (`backend/app/services/telemetry_simulator.py`)

**Mimics**: IoT Devices / Data Producers

Generates realistic telemetry data every 5 seconds for active vehicles:
- GPS coordinates (latitude/longitude)
- Speed (km/h)
- Battery level (%)
- Heading (degrees)
- Odometer reading (km)

**Data Flow**:
```
Simulator → Database → Event Queue → Event Handlers → WebSocket Clients
```

### 4. WebSocket Streaming (`backend/app/api/websocket.py`)

**Mimics**: Kafka Streams / Real-time Data Pipeline

The WebSocket endpoint (`ws://localhost:8000/ws/telemetry`) provides:
- **Real-time streaming** of telemetry events to frontend clients
- **Multiple subscribers** (multiple browser tabs can connect)
- **Event filtering** by type (telemetry, alerts, vehicle status)

## How It Works

### Data Flow Diagram

```
┌─────────────────────┐
│ Telemetry Simulator │ (Every 5 seconds)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   MySQL Database    │ (Persistent storage)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Event Queue      │ (In-memory pub/sub)
│  (Kafka-like Topic) │
└──────────┬──────────┘
           │
           ├─────────────────────┐
           │                     │
           ▼                     ▼
┌──────────────────┐   ┌──────────────────┐
│  Event Handlers  │   │  WebSocket API   │
│  (Consumers)     │   │  (Stream)        │
└──────────────────┘   └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Frontend Clients│
                       │  (React App)     │
                       └──────────────────┘
```

### Event Processing Flow

1. **Data Generation**:
   - Telemetry simulator generates data for each active vehicle
   - Data is saved to MySQL database
   - Event is published to the event queue

2. **Event Distribution**:
   - Event queue receives the event
   - All subscribed handlers are notified
   - Handlers process events concurrently

3. **Real-time Streaming**:
   - WebSocket handler receives telemetry events
   - Events are broadcast to all connected clients
   - Frontend displays data in real-time

## Comparison with Confluent Kafka

| Feature | Our Implementation | Confluent Kafka |
|---------|-------------------|-----------------|
| **Message Queue** | `asyncio.Queue` | Distributed log |
| **Topics** | `EventType` enum | Named topics |
| **Producers** | `event_queue.publish()` | Kafka Producer API |
| **Consumers** | Event handlers | Consumer Groups |
| **Persistence** | MySQL database | Kafka log segments |
| **Streaming** | WebSocket | Kafka Streams |
| **Scalability** | Single process | Distributed cluster |
| **Durability** | Database-backed | Replicated logs |

## Key Advantages of This Approach

### For Development/Demo:
1. **No external dependencies** - No Kafka cluster needed
2. **Fast startup** - Runs in Docker containers
3. **Easy debugging** - All logs in one place
4. **Cost-effective** - No cloud Kafka service fees

### For Learning:
1. **Clear code** - Easy to understand pub/sub concepts
2. **Visible data flow** - Can see events in real-time
3. **Modifiable** - Easy to add new event types
4. **Testable** - Simple to write unit tests

## Viewing Real-Time Telemetry

### Frontend (React)
Navigate to: **http://localhost:3000/telemetry**

You'll see:
- Live telemetry cards for each active vehicle
- Updates every 5 seconds
- Connection status indicator
- Event counter

### Backend Logs
```bash
docker-compose logs -f backend | grep telemetry
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/telemetry');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Telemetry:', data);
};
```

## Event Types and Use Cases

### 1. TELEMETRY_RECEIVED
**Use Case**: Real-time vehicle tracking
- GPS location updates
- Battery monitoring
- Speed tracking
- Odometer readings

### 2. VEHICLE_STATUS_CHANGED
**Use Case**: Fleet state management
- Vehicle goes online/offline
- Maintenance mode activation
- Status transitions

### 3. ALERT_CREATED
**Use Case**: Proactive monitoring
- Low battery warnings
- Maintenance reminders
- System errors
- Critical alerts

### 4. ASSIGNMENT_CREATED/COMPLETED
**Use Case**: Route management
- New route assignments
- Completion tracking
- Performance metrics

## Extending the System

### Adding a New Event Type

1. **Define the event type**:
```python
class EventType(str, Enum):
    NEW_EVENT_TYPE = "new_event_type"
```

2. **Create a handler**:
```python
async def handle_new_event(event: Event):
    # Process event
    logger.info(f"New event: {event.data}")
```

3. **Register the handler**:
```python
event_queue.subscribe(EventType.NEW_EVENT_TYPE, handle_new_event)
```

4. **Publish events**:
```python
await event_queue.publish(Event(
    event_type=EventType.NEW_EVENT_TYPE,
    data={'key': 'value'},
    timestamp=datetime.utcnow(),
    event_id=str(uuid.uuid4())
))
```

## Production Considerations

For production deployment, consider:

1. **Replace with actual Kafka** for:
   - Horizontal scalability
   - Message persistence
   - Fault tolerance
   - Multi-datacenter replication

2. **Add message schemas** using:
   - Avro
   - Protocol Buffers
   - JSON Schema

3. **Implement**:
   - Dead letter queues
   - Retry mechanisms
   - Circuit breakers
   - Rate limiting

4. **Monitoring**:
   - Event throughput metrics
   - Consumer lag monitoring
   - Error rate tracking
   - Performance profiling

## Summary

This implementation demonstrates core pub/sub concepts using lightweight, easy-to-understand Python code. It's perfect for:
- **DevOps demonstrations**
- **Learning event-driven architecture**
- **Prototyping real-time systems**
- **Local development and testing**

The architecture can be easily migrated to Confluent Kafka or other message brokers when scaling requirements demand it.

---

**Made with Bob** - Fleet Management Platform