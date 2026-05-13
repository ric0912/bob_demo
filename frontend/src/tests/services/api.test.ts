import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import axios from 'axios';
import { api } from '../../services/api';

// Mock axios
vi.mock('axios');
const mockedAxios = vi.mocked(axios, true);

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('Vehicle API', () => {
    it('should fetch vehicles successfully', async () => {
      const mockVehicles = [
        {
          id: '1',
          vin: '1HGBH41JXMN109186',
          make: 'Tesla',
          model: 'Model 3',
          year: 2023,
          status: 'active'
        }
      ];

      mockedAxios.get.mockResolvedValue({ data: mockVehicles });

      const result = await api.get('/vehicles');
      
      expect(result.data).toEqual(mockVehicles);
      expect(mockedAxios.get).toHaveBeenCalledWith('/vehicles');
    });

    it('should create vehicle successfully', async () => {
      const newVehicle = {
        vin: '1HGBH41JXMN109186',
        make: 'Tesla',
        model: 'Model 3',
        year: 2023,
        status: 'idle',
        battery_capacity: 75.5
      };

      const createdVehicle = { id: '1', ...newVehicle };
      mockedAxios.post.mockResolvedValue({ data: createdVehicle });

      const result = await api.post('/vehicles', newVehicle);
      
      expect(result.data).toEqual(createdVehicle);
      expect(mockedAxios.post).toHaveBeenCalledWith('/vehicles', newVehicle);
    });

    it('should update vehicle successfully', async () => {
      const vehicleId = '1';
      const updateData = { status: 'maintenance' };
      const updatedVehicle = {
        id: vehicleId,
        vin: '1HGBH41JXMN109186',
        make: 'Tesla',
        model: 'Model 3',
        year: 2023,
        status: 'maintenance',
        battery_capacity: 75.5
      };

      mockedAxios.put.mockResolvedValue({ data: updatedVehicle });

      const result = await api.put(`/vehicles/${vehicleId}`, updateData);
      
      expect(result.data).toEqual(updatedVehicle);
      expect(mockedAxios.put).toHaveBeenCalledWith(`/vehicles/${vehicleId}`, updateData);
    });

    it('should delete vehicle successfully', async () => {
      const vehicleId = '1';
      mockedAxios.delete.mockResolvedValue({ data: null });

      await api.delete(`/vehicles/${vehicleId}`);
      
      expect(mockedAxios.delete).toHaveBeenCalledWith(`/vehicles/${vehicleId}`);
    });

    it('should handle API errors', async () => {
      const errorMessage = 'Network Error';
      mockedAxios.get.mockRejectedValue(new Error(errorMessage));

      await expect(api.get('/vehicles')).rejects.toThrow(errorMessage);
    });
  });

  describe('Telemetry API', () => {
    it('should fetch telemetry data', async () => {
      const mockTelemetry = [
        {
          vehicle_id: '1',
          latitude: 37.7749,
          longitude: -122.4194,
          speed: 45.5,
          battery_level: 85.0,
          timestamp: '2023-01-01T00:00:00Z'
        }
      ];

      mockedAxios.get.mockResolvedValue({ data: mockTelemetry });

      const result = await api.get('/telemetry');
      
      expect(result.data).toEqual(mockTelemetry);
    });

    it('should submit telemetry data', async () => {
      const telemetryData = {
        vehicle_id: '1',
        latitude: 37.7749,
        longitude: -122.4194,
        speed: 45.5,
        battery_level: 85.0
      };

      mockedAxios.post.mockResolvedValue({ data: telemetryData });

      const result = await api.post('/telemetry', telemetryData);
      
      expect(result.data).toEqual(telemetryData);
      expect(mockedAxios.post).toHaveBeenCalledWith('/telemetry', telemetryData);
    });

    it('should fetch vehicle-specific telemetry', async () => {
      const vehicleId = '1';
      const mockTelemetry = [
        {
          vehicle_id: vehicleId,
          latitude: 37.7749,
          longitude: -122.4194,
          speed: 45.5,
          battery_level: 85.0
        }
      ];

      mockedAxios.get.mockResolvedValue({ data: mockTelemetry });

      const result = await api.get(`/telemetry/vehicle/${vehicleId}`);
      
      expect(result.data).toEqual(mockTelemetry);
    });
  });

  describe('Fleet API', () => {
    it('should fetch fleet overview', async () => {
      const mockOverview = {
        total_vehicles: 10,
        active_assignments: 5,
        vehicle_status: {
          active: 5,
          idle: 3,
          maintenance: 2
        }
      };

      mockedAxios.get.mockResolvedValue({ data: mockOverview });

      const result = await api.get('/fleet/overview');
      
      expect(result.data).toEqual(mockOverview);
    });

    it('should create fleet assignment', async () => {
      const assignmentData = {
        vehicle_id: '1',
        route_id: 'route-123',
        driver_id: 'driver-456',
        status: 'assigned'
      };

      const createdAssignment = { id: 'assignment-1', ...assignmentData };
      mockedAxios.post.mockResolvedValue({ data: createdAssignment });

      const result = await api.post('/fleet/assignments', assignmentData);
      
      expect(result.data).toEqual(createdAssignment);
    });

    it('should fetch alerts', async () => {
      const mockAlerts = [
        {
          id: 'alert-1',
          vehicle_id: '1',
          alert_type: 'low_battery',
          severity: 'warning',
          message: 'Battery low',
          acknowledged: false
        }
      ];

      mockedAxios.get.mockResolvedValue({ data: mockAlerts });

      const result = await api.get('/fleet/alerts');
      
      expect(result.data).toEqual(mockAlerts);
    });

    it('should acknowledge alert', async () => {
      const alertId = 'alert-1';
      const response = { message: 'Alert acknowledged', alert_id: alertId };

      mockedAxios.post.mockResolvedValue({ data: response });

      const result = await api.post(`/fleet/alerts/${alertId}/acknowledge`);
      
      expect(result.data).toEqual(response);
    });
  });

  describe('Analytics API', () => {
    it('should fetch analytics summary', async () => {
      const mockSummary = {
        total_vehicles: 10,
        active_vehicles: 5,
        total_telemetry_records: 1000,
        completed_assignments_30d: 50,
        critical_alerts: 2,
        average_battery_level: 85.5
      };

      mockedAxios.get.mockResolvedValue({ data: mockSummary });

      const result = await api.get('/analytics/summary');
      
      expect(result.data).toEqual(mockSummary);
    });

    it('should fetch vehicle analytics', async () => {
      const vehicleId = '1';
      const mockAnalytics = {
        vehicle_id: vehicleId,
        vin: '1HGBH41JXMN109186',
        period_days: 7,
        telemetry_records: 100,
        average_speed: 45.5,
        total_distance: 500.0,
        assignments_completed: 5,
        alerts_generated: 2
      };

      mockedAxios.get.mockResolvedValue({ data: mockAnalytics });

      const result = await api.get(`/analytics/vehicle/${vehicleId}`);
      
      expect(result.data).toEqual(mockAnalytics);
    });

    it('should fetch performance metrics', async () => {
      const mockMetrics = {
        period_days: 7,
        avg_assignment_completion_seconds: 7200,
        vehicle_utilization_rate: 75.5,
        alerts_per_day: 2.5
      };

      mockedAxios.get.mockResolvedValue({ data: mockMetrics });

      const result = await api.get('/analytics/performance');
      
      expect(result.data).toEqual(mockMetrics);
    });

    it('should fetch trends data', async () => {
      const mockTrends = {
        period_days: 30,
        telemetry_trend: [
          { date: '2023-01-01', count: 100 },
          { date: '2023-01-02', count: 120 }
        ],
        assignments_trend: [
          { date: '2023-01-01', count: 5 },
          { date: '2023-01-02', count: 7 }
        ],
        alerts_trend: [
          { date: '2023-01-01', count: 2 },
          { date: '2023-01-02', count: 1 }
        ]
      };

      mockedAxios.get.mockResolvedValue({ data: mockTrends });

      const result = await api.get('/analytics/trends');
      
      expect(result.data).toEqual(mockTrends);
    });
  });

  describe('Error Handling', () => {
    it('should handle 404 errors', async () => {
      const error = {
        response: {
          status: 404,
          data: { detail: 'Vehicle not found' }
        }
      };

      mockedAxios.get.mockRejectedValue(error);

      await expect(api.get('/vehicles/non-existent')).rejects.toMatchObject(error);
    });

    it('should handle 400 errors', async () => {
      const error = {
        response: {
          status: 400,
          data: { detail: 'Invalid data' }
        }
      };

      mockedAxios.post.mockRejectedValue(error);

      await expect(api.post('/vehicles', {})).rejects.toMatchObject(error);
    });

    it('should handle 500 errors', async () => {
      const error = {
        response: {
          status: 500,
          data: { detail: 'Internal server error' }
        }
      };

      mockedAxios.get.mockRejectedValue(error);

      await expect(api.get('/vehicles')).rejects.toMatchObject(error);
    });

    it('should handle network errors', async () => {
      const error = new Error('Network Error');
      mockedAxios.get.mockRejectedValue(error);

      await expect(api.get('/vehicles')).rejects.toThrow('Network Error');
    });
  });
});

// Made with Bob
