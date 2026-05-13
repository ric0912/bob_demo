-- Fleet Management Platform Database Initialization Script

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS fleet_management;
USE fleet_management;

-- Vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    id VARCHAR(36) PRIMARY KEY,
    vin VARCHAR(17) UNIQUE NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    license_plate VARCHAR(20),
    status ENUM('ACTIVE', 'IDLE', 'MAINTENANCE', 'OFFLINE') DEFAULT 'IDLE' NOT NULL,
    battery_capacity DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_vin (vin),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Telemetry table
CREATE TABLE IF NOT EXISTS telemetry (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id VARCHAR(36) NOT NULL,
    latitude DECIMAL(10,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL,
    speed DECIMAL(5,2),
    battery_level DECIMAL(5,2),
    heading DECIMAL(5,2),
    odometer DECIMAL(10,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    INDEX idx_vehicle_timestamp (vehicle_id, timestamp),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Fleet assignments table
CREATE TABLE IF NOT EXISTS fleet_assignments (
    id VARCHAR(36) PRIMARY KEY,
    vehicle_id VARCHAR(36) NOT NULL,
    route_id VARCHAR(36),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    status ENUM('ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED') DEFAULT 'ASSIGNED' NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    INDEX idx_vehicle_id (vehicle_id),
    INDEX idx_status (status),
    INDEX idx_assigned_at (assigned_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Alerts table
CREATE TABLE IF NOT EXISTS alerts (
    id VARCHAR(36) PRIMARY KEY,
    vehicle_id VARCHAR(36) NOT NULL,
    alert_type ENUM('BATTERY_LOW', 'MAINTENANCE_REQUIRED', 'SENSOR_FAILURE', 'SYSTEM_ERROR') NOT NULL,
    severity ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL,
    message TEXT,
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    INDEX idx_vehicle_severity (vehicle_id, severity),
    INDEX idx_acknowledged (acknowledged),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data for demonstration
-- All vehicles are Toyota brand with realistic specifications
INSERT INTO vehicles (id, vin, make, model, year, license_plate, status, battery_capacity) VALUES
('550e8400-e29b-41d4-a716-446655440001', '5TDJZ3DC8PS123456', 'Toyota', 'Camry Hybrid', 2024, 'TYT-001', 'ACTIVE', 72.50),
('550e8400-e29b-41d4-a716-446655440002', '4T1B11HK5KU234567', 'Toyota', 'Prius Prime', 2024, 'TYT-002', 'IDLE', 68.00),
('550e8400-e29b-41d4-a716-446655440003', '5YFBURHE8LP345678', 'Toyota', 'Corolla Hybrid', 2024, 'TYT-003', 'ACTIVE', 65.00),
('550e8400-e29b-41d4-a716-446655440004', '5TDDZ3DC2NS456789', 'Toyota', 'Highlander Hybrid', 2024, 'TYT-004', 'MAINTENANCE', 85.00),
('550e8400-e29b-41d4-a716-446655440005', 'JTMEB3FV8PD567890', 'Toyota', 'RAV4 Prime', 2024, 'TYT-005', 'IDLE', 78.00),
('550e8400-e29b-41d4-a716-446655440006', '5TDJZ3DC1PS678901', 'Toyota', 'Camry Hybrid', 2023, 'TYT-006', 'ACTIVE', 72.50),
('550e8400-e29b-41d4-a716-446655440007', '4T1B11HK2KU789012', 'Toyota', 'Prius Prime', 2023, 'TYT-007', 'IDLE', 68.00),
('550e8400-e29b-41d4-a716-446655440008', 'JTMRB3FV5ND890123', 'Toyota', 'RAV4 Hybrid', 2024, 'TYT-008', 'ACTIVE', 75.00),
('550e8400-e29b-41d4-a716-446655440009', '5TDDZ3DC5NS901234', 'Toyota', 'Highlander Hybrid', 2023, 'TYT-009', 'OFFLINE', 85.00),
('550e8400-e29b-41d4-a716-446655440010', '5YFBURHE5LP012345', 'Toyota', 'Corolla Hybrid', 2023, 'TYT-010', 'IDLE', 65.00);

-- Insert sample telemetry data for Toyota vehicles
INSERT INTO telemetry (vehicle_id, latitude, longitude, speed, battery_level, heading, odometer) VALUES
-- Camry Hybrid TYT-001 (Active)
('550e8400-e29b-41d4-a716-446655440001', 37.7749, -122.4194, 45.50, 70.00, 180.00, 12450.50),
('550e8400-e29b-41d4-a716-446655440001', 37.7759, -122.4184, 48.00, 69.80, 185.00, 12452.00),
('550e8400-e29b-41d4-a716-446655440001', 37.7769, -122.4174, 50.00, 69.60, 190.00, 12453.50),
-- Prius Prime TYT-002 (Idle)
('550e8400-e29b-41d4-a716-446655440002', 37.7849, -122.4094, 0.00, 85.00, 90.00, 8250.25),
('550e8400-e29b-41d4-a716-446655440002', 37.7849, -122.4094, 0.00, 85.00, 90.00, 8250.25),
-- Corolla Hybrid TYT-003 (Active)
('550e8400-e29b-41d4-a716-446655440003', 37.7649, -122.4294, 55.00, 62.00, 270.00, 15100.75),
('550e8400-e29b-41d4-a716-446655440003', 37.7659, -122.4284, 52.00, 61.70, 275.00, 15102.25),
('550e8400-e29b-41d4-a716-446655440003', 37.7669, -122.4274, 48.00, 61.40, 280.00, 15103.75),
-- Highlander Hybrid TYT-004 (Maintenance)
('550e8400-e29b-41d4-a716-446655440004', 37.7550, -122.4350, 0.00, 78.00, 0.00, 9875.00),
-- RAV4 Prime TYT-005 (Idle)
('550e8400-e29b-41d4-a716-446655440005', 37.7950, -122.4000, 0.00, 76.00, 45.00, 11200.50),
-- Camry Hybrid TYT-006 (Active)
('550e8400-e29b-41d4-a716-446655440006', 37.7800, -122.4150, 42.00, 68.00, 135.00, 18750.25),
('550e8400-e29b-41d4-a716-446655440006', 37.7810, -122.4140, 44.00, 67.80, 140.00, 18751.75),
-- Prius Prime TYT-007 (Idle)
('550e8400-e29b-41d4-a716-446655440007', 37.7700, -122.4250, 0.00, 82.00, 180.00, 7650.00),
-- RAV4 Hybrid TYT-008 (Active)
('550e8400-e29b-41d4-a716-446655440008', 37.7600, -122.4400, 38.00, 72.00, 225.00, 13500.50),
('550e8400-e29b-41d4-a716-446655440008', 37.7590, -122.4410, 40.00, 71.80, 230.00, 13502.00),
('550e8400-e29b-41d4-a716-446655440008', 37.7580, -122.4420, 42.00, 71.60, 235.00, 13503.50),
-- Highlander Hybrid TYT-009 (Offline - no recent telemetry)
-- Corolla Hybrid TYT-010 (Idle)
('550e8400-e29b-41d4-a716-446655440010', 37.7900, -122.4100, 0.00, 63.00, 315.00, 16800.00);

-- Insert sample fleet assignments for Toyota vehicles
INSERT INTO fleet_assignments (id, vehicle_id, route_id, status) VALUES
('650e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'route-sf-downtown', 'IN_PROGRESS'),
('650e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440003', 'route-sf-airport', 'IN_PROGRESS'),
('650e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440006', 'route-sf-marina', 'IN_PROGRESS'),
('650e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440008', 'route-sf-mission', 'IN_PROGRESS');

-- Insert sample alerts for Toyota vehicles
INSERT INTO alerts (id, vehicle_id, alert_type, severity, message, acknowledged) VALUES
('750e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440003', 'BATTERY_LOW', 'HIGH', 'Corolla Hybrid TYT-003: Battery level below 65%', FALSE),
('750e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440004', 'MAINTENANCE_REQUIRED', 'MEDIUM', 'Highlander Hybrid TYT-004: Scheduled 10,000 mile service due', FALSE),
('750e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440010', 'BATTERY_LOW', 'MEDIUM', 'Corolla Hybrid TYT-010: Battery level at 63%', FALSE),
('750e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440009', 'SYSTEM_ERROR', 'CRITICAL', 'Highlander Hybrid TYT-009: Vehicle offline - no telemetry received', FALSE);

-- Create views for common queries
CREATE OR REPLACE VIEW active_vehicles_summary AS
SELECT 
    v.id,
    v.vin,
    v.make,
    v.model,
    v.status,
    t.latitude,
    t.longitude,
    t.speed,
    t.battery_level,
    t.timestamp as last_telemetry
FROM vehicles v
LEFT JOIN (
    SELECT vehicle_id, latitude, longitude, speed, battery_level, timestamp,
           ROW_NUMBER() OVER (PARTITION BY vehicle_id ORDER BY timestamp DESC) as rn
    FROM telemetry
) t ON v.id = t.vehicle_id AND t.rn = 1
WHERE v.status IN ('ACTIVE', 'IDLE');

-- Grant privileges (if needed)
-- GRANT ALL PRIVILEGES ON fleet_management.* TO 'fleetuser'@'%';
-- FLUSH PRIVILEGES;

SELECT 'Database initialization completed successfully!' as status;

-- Made with Bob
