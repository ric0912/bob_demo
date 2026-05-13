import { useEffect, useState, useRef } from 'react';
import {
  Grid,
  Column,
  Tile,
  Tag,
  InlineNotification
} from '@carbon/react';
import {
  Activity,
  ChargingStation,
  DirectionRotaryRight,
  Meter,
  Location,
  Time
} from '@carbon/icons-react';
import { api } from '../services/api';

interface TelemetryData {
  vehicle_id: string;
  latitude: number;
  longitude: number;
  speed: number;
  battery_level: number;
  heading: number;
  odometer: number;
  timestamp: string;
}

interface TelemetryEvent {
  type: string;
  event_id: string;
  timestamp: string;
  data: TelemetryData;
}

interface VehicleInfo {
  id: string;
  vin: string;
  make: string;
  model: string;
  year: number;
  license_plate?: string;
  status: string;
}

export default function TelemetryStream() {
  const [telemetryData, setTelemetryData] = useState<Map<string, TelemetryData>>(new Map());
  const [vehicles, setVehicles] = useState<Map<string, VehicleInfo>>(new Map());
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');
  const [eventCount, setEventCount] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);

  // Fetch vehicle information
  useEffect(() => {
    const fetchVehicles = async () => {
      try {
        const vehicleList = await api.getVehicles();
        const vehicleMap = new Map<string, VehicleInfo>();
        vehicleList.forEach((vehicle) => {
          vehicleMap.set(vehicle.id, vehicle);
        });
        setVehicles(vehicleMap);
      } catch (error) {
        console.error('Error fetching vehicles:', error);
      }
    };
    fetchVehicles();
  }, []);

  useEffect(() => {
    // Connect to WebSocket
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8000/ws/telemetry');
      wsRef.current = ws;

      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnectionStatus('connected');
      };

      ws.onmessage = (event) => {
        const message: TelemetryEvent = JSON.parse(event.data);
        
        if (message.type === 'telemetry') {
          setTelemetryData((prev) => {
            const newMap = new Map(prev);
            newMap.set(message.data.vehicle_id, message.data);
            return newMap;
          });
          setEventCount((prev) => prev + 1);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setConnectionStatus('disconnected');
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnectionStatus('disconnected');
        
        // Attempt to reconnect after 5 seconds
        setTimeout(() => {
          console.log('Attempting to reconnect...');
          connectWebSocket();
        }, 5000);
      };
    };

    connectWebSocket();

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const getBatteryColor = (level: number) => {
    if (level > 70) return '#24a148';
    if (level > 40) return '#f1c21b';
    return '#da1e28';
  };

  const getStatusColor = (status: string) => {
    switch (status?.toUpperCase()) {
      case 'ACTIVE': return '#24a148';
      case 'IDLE': return '#0f62fe';
      case 'MAINTENANCE': return '#f1c21b';
      case 'OFFLINE': return '#da1e28';
      default: return '#8d8d8d';
    }
  };

  const getDirectionLabel = (heading: number) => {
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const index = Math.round(heading / 45) % 8;
    return directions[index];
  };

  return (
    <>
      <Grid>
        <Column lg={16}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
            <div>
              <h1 style={{ fontSize: '2.5rem', fontWeight: '300', marginBottom: '0.5rem' }}>
                🚗 Real-Time Telemetry Stream
              </h1>
              <p style={{ fontSize: '0.875rem', opacity: 0.7 }}>
                Live vehicle data updates every 5 seconds
              </p>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
              <div className="status-indicator">
                <div
                  className={connectionStatus === 'connected' ? 'status-dot pulse-animation' : 'status-dot'}
                  style={{
                    backgroundColor: 
                      connectionStatus === 'connected' ? '#24a148' :
                      connectionStatus === 'connecting' ? '#f1c21b' :
                      '#da1e28'
                  }}
                />
                <Tag
                  type={
                    connectionStatus === 'connected' ? 'green' :
                    connectionStatus === 'connecting' ? 'warm-gray' :
                    'red'
                  }
                >
                  {connectionStatus.charAt(0).toUpperCase() + connectionStatus.slice(1)}
                </Tag>
              </div>
              <Tag type="blue">
                📊 Events: {eventCount}
              </Tag>
              <Tag type="purple">
                🚙 Vehicles: {telemetryData.size}
              </Tag>
            </div>
          </div>
        </Column>
      </Grid>

      {connectionStatus === 'disconnected' && (
        <Grid>
          <Column lg={16}>
            <InlineNotification
              kind="error"
              title="Connection Lost"
              subtitle="WebSocket disconnected. Attempting to reconnect..."
              lowContrast
            />
          </Column>
        </Grid>
      )}

      {telemetryData.size === 0 && connectionStatus === 'connected' && (
        <Grid>
          <Column lg={16}>
            <Tile style={{ textAlign: 'center', padding: '3rem' }}>
              <Activity size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
              <p style={{ opacity: 0.6 }}>
                Waiting for telemetry data... (Updates every 5 seconds)
              </p>
            </Tile>
          </Column>
        </Grid>
      )}

      <Grid>
        {Array.from(telemetryData.entries()).map(([vehicleId, data]) => {
          const vehicle = vehicles.get(vehicleId);
          const batteryColor = getBatteryColor(data.battery_level);
          const statusColor = getStatusColor(vehicle?.status || 'UNKNOWN');
          
          return (
            <Column key={vehicleId} sm={4} md={4} lg={5}>
              <Tile className="telemetry-card fade-in" style={{
                height: '100%',
                border: `2px solid ${statusColor}40`,
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
                transition: 'all 0.3s ease',
                position: 'relative',
                overflow: 'hidden'
              }}>
                {/* Status indicator bar */}
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  height: '4px',
                  background: `linear-gradient(90deg, ${statusColor}, ${statusColor}80)`,
                }} />

                {/* Vehicle Header */}
                <div style={{
                  marginBottom: '1rem',
                  paddingTop: '0.5rem'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem' }}>
                    <div style={{ flex: 1 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                        <h3 style={{
                          fontSize: '1.125rem',
                          fontWeight: '600',
                          margin: 0,
                          color: '#161616'
                        }}>
                          {vehicle ? `${vehicle.make} ${vehicle.model}` : 'Unknown Vehicle'}
                        </h3>
                        <Tag
                          type={
                            vehicle?.status === 'ACTIVE' ? 'green' :
                            vehicle?.status === 'IDLE' ? 'blue' :
                            vehicle?.status === 'MAINTENANCE' ? 'warm-gray' :
                            'red'
                          }
                          size="sm"
                        >
                          {vehicle?.status || 'UNKNOWN'}
                        </Tag>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.75rem', opacity: 0.7 }}>
                        <span>🚗 {vehicle?.license_plate || 'N/A'}</span>
                        <span>📅 {vehicle?.year || 'N/A'}</span>
                      </div>
                    </div>
                  </div>

                  {/* Timestamp */}
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.25rem',
                    fontSize: '0.75rem',
                    opacity: 0.6,
                    padding: '0.5rem',
                    backgroundColor: 'rgba(0, 0, 0, 0.03)',
                    borderRadius: '4px'
                  }}>
                    <Time size={14} />
                    <span>Last update: {new Date(data.timestamp).toLocaleTimeString()}</span>
                  </div>
                </div>

                {/* Battery Level Progress Bar */}
                <div style={{ marginBottom: '1rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <ChargingStation size={20} style={{ color: batteryColor }} />
                      <span style={{ fontSize: '0.875rem', fontWeight: '600' }}>Battery Level</span>
                    </div>
                    <span style={{ fontSize: '1.25rem', fontWeight: '700', color: batteryColor }}>
                      {data.battery_level.toFixed(1)}%
                    </span>
                  </div>
                  <div style={{
                    height: '8px',
                    backgroundColor: 'rgba(0, 0, 0, 0.1)',
                    borderRadius: '4px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      height: '100%',
                      width: `${data.battery_level}%`,
                      backgroundColor: batteryColor,
                      transition: 'width 0.3s ease',
                      borderRadius: '4px'
                    }} />
                  </div>
                </div>

                {/* Telemetry Metrics Grid */}
                <Grid condensed style={{ marginBottom: '1rem' }}>
                  <Column sm={2} md={2} lg={8}>
                    <div style={{ 
                      padding: '1rem', 
                      backgroundColor: 'rgba(15, 98, 254, 0.08)',
                      borderRadius: '8px',
                      border: '1px solid rgba(15, 98, 254, 0.2)',
                      height: '100%'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                        <Meter size={20} style={{ color: '#0f62fe' }} />
                        <span style={{ fontSize: '0.75rem', fontWeight: '600', opacity: 0.8 }}>Speed</span>
                      </div>
                      <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#0f62fe' }}>
                        {data.speed.toFixed(1)}
                      </div>
                      <div style={{ fontSize: '0.75rem', opacity: 0.6 }}>km/h</div>
                    </div>
                  </Column>

                  <Column sm={2} md={2} lg={8}>
                    <div style={{ 
                      padding: '1rem', 
                      backgroundColor: 'rgba(241, 194, 27, 0.08)',
                      borderRadius: '8px',
                      border: '1px solid rgba(241, 194, 27, 0.2)',
                      height: '100%'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                        <DirectionRotaryRight size={20} style={{ color: '#f1c21b' }} />
                        <span style={{ fontSize: '0.75rem', fontWeight: '600', opacity: 0.8 }}>Heading</span>
                      </div>
                      <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#f1c21b' }}>
                        {data.heading.toFixed(0)}°
                      </div>
                      <div style={{ fontSize: '0.75rem', opacity: 0.6 }}>{getDirectionLabel(data.heading)}</div>
                    </div>
                  </Column>

                  <Column sm={4} md={4} lg={16}>
                    <div style={{ 
                      padding: '1rem', 
                      backgroundColor: 'rgba(138, 63, 252, 0.08)',
                      borderRadius: '8px',
                      border: '1px solid rgba(138, 63, 252, 0.2)'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                        <Activity size={20} style={{ color: '#8a3ffc' }} />
                        <span style={{ fontSize: '0.75rem', fontWeight: '600', opacity: 0.8 }}>Odometer</span>
                      </div>
                      <div style={{ fontSize: '1.5rem', fontWeight: '700', color: '#8a3ffc' }}>
                        {data.odometer.toFixed(1)} <span style={{ fontSize: '0.875rem' }}>km</span>
                      </div>
                    </div>
                  </Column>
                </Grid>

                {/* GPS Coordinates */}
                <div style={{
                  padding: '0.75rem',
                  backgroundColor: 'rgba(0, 0, 0, 0.03)',
                  borderRadius: '8px',
                  border: '1px solid rgba(0, 0, 0, 0.1)'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <Location size={16} style={{ opacity: 0.6 }} />
                    <span style={{ fontSize: '0.75rem', fontWeight: '600', opacity: 0.6 }}>GPS Coordinates</span>
                  </div>
                  <div style={{ fontSize: '0.875rem', fontFamily: 'monospace', fontWeight: '500' }}>
                    {data.latitude.toFixed(6)}, {data.longitude.toFixed(6)}
                  </div>
                </div>
              </Tile>
            </Column>
          );
        })}
      </Grid>
    </>
  );
}

// Made with Bob