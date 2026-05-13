// Vehicle types
export enum VehicleStatus {
  ACTIVE = 'active',
  IDLE = 'idle',
  MAINTENANCE = 'maintenance',
  OFFLINE = 'offline',
}

export interface Vehicle {
  id: string;
  vin: string;
  make: string;
  model: string;
  year: number;
  license_plate?: string;
  status: VehicleStatus;
  battery_capacity?: number;
  created_at: string;
  updated_at: string;
}

export interface VehicleCreate {
  vin: string;
  make: string;
  model: string;
  year: number;
  license_plate?: string;
  battery_capacity?: number;
  status?: VehicleStatus;
}

// Telemetry types
export interface Telemetry {
  id: number;
  vehicle_id: string;
  latitude: number;
  longitude: number;
  speed?: number;
  battery_level?: number;
  heading?: number;
  odometer?: number;
  timestamp: string;
}

export interface TelemetryCreate {
  vehicle_id: string;
  latitude: number;
  longitude: number;
  speed?: number;
  battery_level?: number;
  heading?: number;
  odometer?: number;
}

// Fleet Assignment types
export enum AssignmentStatus {
  ASSIGNED = 'assigned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

export interface FleetAssignment {
  id: string;
  vehicle_id: string;
  route_id?: string;
  status: AssignmentStatus;
  assigned_at: string;
  completed_at?: string;
}

export interface FleetAssignmentCreate {
  vehicle_id: string;
  route_id?: string;
}

// Alert types
export enum AlertType {
  BATTERY_LOW = 'battery_low',
  MAINTENANCE_REQUIRED = 'maintenance_required',
  SENSOR_FAILURE = 'sensor_failure',
  SYSTEM_ERROR = 'system_error',
}

export enum AlertSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical',
}

export interface Alert {
  id: string;
  vehicle_id: string;
  alert_type: AlertType;
  severity: AlertSeverity;
  message?: string;
  acknowledged: boolean;
  created_at: string;
}

// Analytics types
export interface FleetOverview {
  total_vehicles: number;
  vehicle_status: Record<string, number>;
  active_assignments: number;
  unacknowledged_alerts: Record<string, number>;
}

export interface AnalyticsSummary {
  total_vehicles: number;
  active_vehicles: number;
  total_telemetry_records: number;
  completed_assignments_30d: number;
  critical_alerts: number;
  average_battery_level?: number;
}

export interface VehicleAnalytics {
  vehicle_id: string;
  vin: string;
  period_days: number;
  telemetry_records: number;
  average_speed?: number;
  total_distance?: number;
  assignments_completed: number;
  alerts_generated: number;
}

// Latest telemetry with vehicle info
export interface VehicleWithTelemetry {
  vehicle_id: string;
  vin: string;
  status: VehicleStatus;
  telemetry: {
    latitude: number;
    longitude: number;
    speed?: number;
    battery_level?: number;
    timestamp: string;
  };
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  detail: string;
  type?: string;
}

// Made with Bob
