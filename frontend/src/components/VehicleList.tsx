import { useEffect, useState } from 'react';
import {
  Grid,
  Column,
  Button,
  DataTable,
  Table,
  TableHead,
  TableRow,
  TableHeader,
  TableBody,
  TableCell,
  TableContainer,
  TableToolbar,
  TableToolbarContent,
  TableToolbarSearch,
  Tag,
  SkeletonPlaceholder,
  InlineNotification
} from '@carbon/react';
import { Add, Renew } from '@carbon/icons-react';
import api from '../services/api';
import type { Vehicle } from '../types';

const headers = [
  { key: 'vin', header: 'VIN' },
  { key: 'make_model', header: 'Make & Model' },
  { key: 'year', header: 'Year' },
  { key: 'license_plate', header: 'License Plate' },
  { key: 'status', header: 'Status' },
  { key: 'battery_capacity', header: 'Battery' },
  { key: 'updated_at', header: 'Last Updated' },
];

export default function VehicleList() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadVehicles();
  }, []);

  const loadVehicles = async () => {
    try {
      setError(null);
      setLoading(true);
      const data = await api.getVehicles();
      setVehicles(data);
    } catch (err) {
      setError('Failed to load vehicles');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusTagType = (status: string): 'red' | 'green' | 'blue' | 'warm-gray' | 'gray' => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'green';
      case 'idle':
        return 'blue';
      case 'maintenance':
        return 'warm-gray';
      case 'offline':
        return 'red';
      default:
        return 'gray';
    }
  };

  const rows = vehicles.map((vehicle) => ({
    id: vehicle.id,
    vin: vehicle.vin,
    make_model: `${vehicle.make} ${vehicle.model}`,
    year: vehicle.year.toString(),
    license_plate: vehicle.license_plate || '-',
    status: vehicle.status,
    battery_capacity: vehicle.battery_capacity ? `${vehicle.battery_capacity} kWh` : '-',
    updated_at: new Date(vehicle.updated_at).toLocaleString(),
  }));

  if (loading) {
    return (
      <Grid>
        <Column lg={16}>
          <SkeletonPlaceholder style={{ height: '400px' }} />
        </Column>
      </Grid>
    );
  }

  return (
    <>
      <Grid>
        <Column lg={16}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
            <h1 style={{ fontSize: '2.5rem', fontWeight: '300' }}>Vehicles</h1>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <Button
                kind="secondary"
                renderIcon={Renew}
                onClick={loadVehicles}
                size="md"
              >
                Refresh
              </Button>
              <Button
                kind="primary"
                renderIcon={Add}
                size="md"
              >
                Add Vehicle
              </Button>
            </div>
          </div>
        </Column>
      </Grid>

      {error && (
        <Grid>
          <Column lg={16}>
            <InlineNotification
              kind="error"
              title="Error"
              subtitle={error}
              lowContrast
            />
          </Column>
        </Grid>
      )}

      <Grid>
        <Column lg={16}>
          <DataTable rows={rows} headers={headers}>
            {({
              rows,
              headers,
              getTableProps,
              getHeaderProps,
              getRowProps,
              getTableContainerProps,
            }) => (
              <TableContainer
                title="Fleet Vehicles"
                description="Manage and monitor your autonomous vehicle fleet"
                {...getTableContainerProps()}
              >
                <TableToolbar>
                  <TableToolbarContent>
                    <TableToolbarSearch
                      placeholder="Search vehicles..."
                      persistent
                    />
                  </TableToolbarContent>
                </TableToolbar>
                <Table {...getTableProps()}>
                  <TableHead>
                    <TableRow>
                      {headers.map((header) => (
                        <TableHeader {...getHeaderProps({ header })} key={header.key}>
                          {header.header}
                        </TableHeader>
                      ))}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {rows.map((row) => (
                      <TableRow {...getRowProps({ row })} key={row.id}>
                        {row.cells.map((cell) => {
                          if (cell.info.header === 'vin') {
                            return (
                              <TableCell key={cell.id} style={{ fontFamily: 'monospace', fontSize: '0.875rem' }}>
                                {cell.value}
                              </TableCell>
                            );
                          }
                          if (cell.info.header === 'status') {
                            return (
                              <TableCell key={cell.id}>
                                <Tag type={getStatusTagType(cell.value as string)}>
                                  {cell.value}
                                </Tag>
                              </TableCell>
                            );
                          }
                          if (cell.info.header === 'updated_at') {
                            return (
                              <TableCell key={cell.id} style={{ fontSize: '0.875rem', opacity: 0.8 }}>
                                {cell.value}
                              </TableCell>
                            );
                          }
                          return <TableCell key={cell.id}>{cell.value}</TableCell>;
                        })}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </DataTable>

          {vehicles.length === 0 && !loading && (
            <div style={{ 
              textAlign: 'center', 
              padding: '4rem', 
              backgroundColor: 'rgba(0, 0, 0, 0.02)',
              borderRadius: '4px',
              marginTop: '1rem'
            }}>
              <Add size={48} style={{ opacity: 0.3, marginBottom: '1rem' }} />
              <p style={{ opacity: 0.6, fontSize: '1.125rem' }}>No vehicles found</p>
              <p style={{ opacity: 0.5, fontSize: '0.875rem', marginTop: '0.5rem' }}>
                Add your first vehicle to get started
              </p>
            </div>
          )}
        </Column>
      </Grid>
    </>
  );
}

// Made with Bob
