import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  Vehicle,
  VehicleCreate,
  Telemetry,
  TelemetryCreate,
  FleetAssignment,
  FleetAssignmentCreate,
  Alert,
  FleetOverview,
  AnalyticsSummary,
  VehicleAnalytics,
  VehicleWithTelemetry,
} from '../types';

// Support runtime configuration from window.ENV (injected by container)
// or fall back to build-time env var or localhost
const API_URL = (window as any).ENV?.VITE_API_URL || import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Handle unauthorized
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Health check
  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Vehicle endpoints
  async getVehicles(skip = 0, limit = 100): Promise<Vehicle[]> {
    const response = await this.client.get('/api/v1/vehicles', {
      params: { skip, limit },
    });
    return response.data;
  }

  async getVehicle(id: string): Promise<Vehicle> {
    const response = await this.client.get(`/api/v1/vehicles/${id}`);
    return response.data;
  }

  async createVehicle(vehicle: VehicleCreate): Promise<Vehicle> {
    const response = await this.client.post('/api/v1/vehicles', vehicle);
    return response.data;
  }

  async updateVehicle(id: string, vehicle: Partial<VehicleCreate>): Promise<Vehicle> {
    const response = await this.client.put(`/api/v1/vehicles/${id}`, vehicle);
    return response.data;
  }

  async deleteVehicle(id: string): Promise<void> {
    await this.client.delete(`/api/v1/vehicles/${id}`);
  }

  async getVehicleStatus(id: string) {
    const response = await this.client.get(`/api/v1/vehicles/${id}/status`);
    return response.data;
  }

  // Telemetry endpoints
  async getTelemetry(vehicleId?: string, skip = 0, limit = 100): Promise<Telemetry[]> {
    const response = await this.client.get('/api/v1/telemetry', {
      params: { vehicle_id: vehicleId, skip, limit },
    });
    return response.data;
  }

  async createTelemetry(telemetry: TelemetryCreate): Promise<Telemetry> {
    const response = await this.client.post('/api/v1/telemetry', telemetry);
    return response.data;
  }

  async getVehicleTelemetry(vehicleId: string, limit = 100): Promise<Telemetry[]> {
    const response = await this.client.get(`/api/v1/telemetry/vehicle/${vehicleId}`, {
      params: { limit },
    });
    return response.data;
  }

  async getLatestTelemetry(): Promise<VehicleWithTelemetry[]> {
    const response = await this.client.get('/api/v1/telemetry/latest');
    return response.data;
  }

  // Fleet endpoints
  async getFleetOverview(): Promise<FleetOverview> {
    const response = await this.client.get('/api/v1/fleet/overview');
    return response.data;
  }

  async getAssignments(skip = 0, limit = 100): Promise<FleetAssignment[]> {
    const response = await this.client.get('/api/v1/fleet/assignments', {
      params: { skip, limit },
    });
    return response.data;
  }

  async createAssignment(assignment: FleetAssignmentCreate): Promise<FleetAssignment> {
    const response = await this.client.post('/api/v1/fleet/assignments', assignment);
    return response.data;
  }

  async updateAssignment(
    id: string,
    assignment: Partial<FleetAssignmentCreate>
  ): Promise<FleetAssignment> {
    const response = await this.client.put(`/api/v1/fleet/assignments/${id}`, assignment);
    return response.data;
  }

  async getAlerts(acknowledged = false, skip = 0, limit = 100): Promise<Alert[]> {
    const response = await this.client.get('/api/v1/fleet/alerts', {
      params: { acknowledged, skip, limit },
    });
    return response.data;
  }

  async acknowledgeAlert(id: string) {
    const response = await this.client.post(`/api/v1/fleet/alerts/${id}/acknowledge`);
    return response.data;
  }

  // Analytics endpoints
  async getAnalyticsSummary(): Promise<AnalyticsSummary> {
    const response = await this.client.get('/api/v1/analytics/summary');
    return response.data;
  }

  async getVehicleAnalytics(vehicleId: string, days = 7): Promise<VehicleAnalytics> {
    const response = await this.client.get(`/api/v1/analytics/vehicle/${vehicleId}`, {
      params: { days },
    });
    return response.data;
  }

  async getPerformanceMetrics(days = 7) {
    const response = await this.client.get('/api/v1/analytics/performance', {
      params: { days },
    });
    return response.data;
  }

  async getTrends(days = 30) {
    const response = await this.client.get('/api/v1/analytics/trends', {
      params: { days },
    });
    return response.data;
  }
}

export const api = new ApiService();
export default api;

// Made with Bob
