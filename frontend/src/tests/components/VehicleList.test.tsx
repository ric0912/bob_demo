import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { VehicleList } from '../../components/VehicleList';
import * as api from '../../services/api';

// Mock the API module
vi.mock('../../services/api');

describe('VehicleList Component', () => {
  const mockVehicles = [
    {
      id: '1',
      vin: '1HGBH41JXMN109186',
      make: 'Tesla',
      model: 'Model 3',
      year: 2023,
      license_plate: 'ABC123',
      status: 'active',
      battery_capacity: 75.5,
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z'
    },
    {
      id: '2',
      vin: '1HGBH41JXMN109187',
      make: 'Tesla',
      model: 'Model Y',
      year: 2023,
      license_plate: 'XYZ789',
      status: 'idle',
      battery_capacity: 80.0,
      created_at: '2023-01-02T00:00:00Z',
      updated_at: '2023-01-02T00:00:00Z'
    }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render loading state initially', () => {
    vi.mocked(api.getVehicles).mockReturnValue(new Promise(() => {}));
    
    render(<VehicleList />);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  it('should render vehicle list after loading', async () => {
    vi.mocked(api.getVehicles).mockResolvedValue(mockVehicles);
    
    render(<VehicleList />);
    
    await waitFor(() => {
      expect(screen.getByText('Tesla Model 3')).toBeInTheDocument();
      expect(screen.getByText('Tesla Model Y')).toBeInTheDocument();
    });
  });

  it('should display vehicle status correctly', async () => {
    vi.mocked(api.getVehicles).mockResolvedValue(mockVehicles);
    
    render(<VehicleList />);
    
    await waitFor(() => {
      expect(screen.getByText('active')).toBeInTheDocument();
      expect(screen.getByText('idle')).toBeInTheDocument();
    });
  });

  it('should handle API errors gracefully', async () => {
    const errorMessage = 'Failed to fetch vehicles';
    vi.mocked(api.getVehicles).mockRejectedValue(new Error(errorMessage));
    
    render(<VehicleList />);
    
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });

  it('should display empty state when no vehicles', async () => {
    vi.mocked(api.getVehicles).mockResolvedValue([]);
    
    render(<VehicleList />);
    
    await waitFor(() => {
      expect(screen.getByText(/no vehicles/i)).toBeInTheDocument();
    });
  });

  it('should display battery capacity for each vehicle', async () => {
    vi.mocked(api.getVehicles).mockResolvedValue(mockVehicles);
    
    render(<VehicleList />);
    
    await waitFor(() => {
      expect(screen.getByText(/75\.5/)).toBeInTheDocument();
      expect(screen.getByText(/80\.0/)).toBeInTheDocument();
    });
  });
});

// Made with Bob
