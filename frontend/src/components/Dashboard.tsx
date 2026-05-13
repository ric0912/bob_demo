import { useEffect, useState } from 'react';
import {
  Grid,
  Column,
  Tile,
  SkeletonPlaceholder,
  InlineNotification,
  Tag
} from '@carbon/react';
import {
  Car,
  Activity,
  WarningAlt,
  ArrowUp,
  Checkmark
} from '@carbon/icons-react';
import api from '../services/api';
import type { FleetOverview, AnalyticsSummary } from '../types';

export default function Dashboard() {
  const [overview, setOverview] = useState<FleetOverview | null>(null);
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      setError(null);
      const [overviewData, analyticsData] = await Promise.all([
        api.getFleetOverview(),
        api.getAnalyticsSummary(),
      ]);
      setOverview(overviewData);
      setAnalytics(analyticsData);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Grid>
        <Column lg={16}>
          <SkeletonPlaceholder style={{ height: '200px', marginBottom: '1rem' }} />
          <SkeletonPlaceholder style={{ height: '200px', marginBottom: '1rem' }} />
          <SkeletonPlaceholder style={{ height: '200px' }} />
        </Column>
      </Grid>
    );
  }

  if (error) {
    return (
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
    );
  }

  return (
    <>
      <Grid>
        {/* Page Title */}
        <Column lg={16}>
          <h1 style={{ marginBottom: '2rem', fontSize: '2.5rem', fontWeight: '300' }}>
            Fleet Dashboard
          </h1>
        </Column>

      {/* Key Metrics - 4 columns */}
      <Column sm={4} md={4} lg={4}>
        <Tile className="fade-in" style={{ height: '100%' }}>
          <div className="stat-card-content">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Car size={32} style={{ color: '#0f62fe' }} />
              <span className="stat-label">Total Vehicles</span>
            </div>
            <div className="stat-value" style={{ color: '#0f62fe' }}>
              {overview?.total_vehicles || 0}
            </div>
          </div>
        </Tile>
      </Column>

      <Column sm={4} md={4} lg={4}>
        <Tile className="fade-in" style={{ height: '100%' }}>
          <div className="stat-card-content">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <Activity size={32} style={{ color: '#24a148' }} />
              <span className="stat-label">Active Vehicles</span>
            </div>
            <div className="stat-value" style={{ color: '#24a148' }}>
              {analytics?.active_vehicles || 0}
            </div>
          </div>
        </Tile>
      </Column>

      <Column sm={4} md={4} lg={4}>
        <Tile className="fade-in" style={{ height: '100%' }}>
          <div className="stat-card-content">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <ArrowUp size={32} style={{ color: '#f1c21b' }} />
              <span className="stat-label">Active Assignments</span>
            </div>
            <div className="stat-value" style={{ color: '#f1c21b' }}>
              {overview?.active_assignments || 0}
            </div>
          </div>
        </Tile>
      </Column>

      <Column sm={4} md={4} lg={4}>
        <Tile className="fade-in" style={{ height: '100%' }}>
          <div className="stat-card-content">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <WarningAlt size={32} style={{ color: '#da1e28' }} />
              <span className="stat-label">Critical Alerts</span>
            </div>
            <div className="stat-value" style={{ color: '#da1e28' }}>
              {analytics?.critical_alerts || 0}
            </div>
          </div>
        </Tile>
      </Column>
      </Grid>

      <Grid style={{ marginTop: '2rem' }}>
      {/* Vehicle Status Breakdown */}
      <Column sm={4} md={4} lg={8}>
        <Tile style={{ height: '100%' }}>
          <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>
            Vehicle Status
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {overview?.vehicle_status && Object.entries(overview.vehicle_status).map(([status, count]) => (
              <div key={status} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Tag
                  type={
                    status === 'active' ? 'green' :
                    status === 'idle' ? 'blue' :
                    status === 'maintenance' ? 'warm-gray' :
                    'red'
                  }
                >
                  {status}
                </Tag>
                <span style={{ fontSize: '1.75rem', fontWeight: '600' }}>{count}</span>
              </div>
            ))}
          </div>
        </Tile>
      </Column>

      {/* Unacknowledged Alerts */}
      <Column sm={4} md={4} lg={8}>
        <Tile style={{ height: '100%' }}>
          <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>
            Unacknowledged Alerts
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {overview?.unacknowledged_alerts && Object.entries(overview.unacknowledged_alerts).map(([severity, count]) => (
              <div key={severity} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Tag
                  type={
                    severity === 'critical' ? 'red' :
                    severity === 'high' ? 'magenta' :
                    severity === 'medium' ? 'warm-gray' :
                    'blue'
                  }
                >
                  {severity}
                </Tag>
                <span style={{ fontSize: '1.75rem', fontWeight: '600' }}>{count}</span>
              </div>
            ))}
            {(!overview?.unacknowledged_alerts || Object.keys(overview.unacknowledged_alerts).length === 0) && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#24a148' }}>
                <Checkmark size={20} />
                <span>No unacknowledged alerts</span>
              </div>
            )}
          </div>
        </Tile>
      </Column>
      </Grid>

      <Grid style={{ marginTop: '2rem' }}>
      {/* Analytics Summary */}
      <Column lg={16}>
        <Tile>
          <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>
            30-Day Summary
          </h3>
          <Grid condensed>
            <Column sm={4} md={4} lg={5}>
              <div style={{ textAlign: 'center', padding: '1rem' }}>
                <div className="stat-label" style={{ marginBottom: '0.5rem' }}>
                  Telemetry Records
                </div>
                <div style={{ fontSize: '2rem', fontWeight: '600', color: '#0f62fe' }}>
                  {analytics?.total_telemetry_records?.toLocaleString() || 0}
                </div>
              </div>
            </Column>
            <Column sm={4} md={4} lg={5}>
              <div style={{ textAlign: 'center', padding: '1rem' }}>
                <div className="stat-label" style={{ marginBottom: '0.5rem' }}>
                  Completed Assignments
                </div>
                <div style={{ fontSize: '2rem', fontWeight: '600', color: '#24a148' }}>
                  {analytics?.completed_assignments_30d || 0}
                </div>
              </div>
            </Column>
            <Column sm={4} md={4} lg={6}>
              <div style={{ textAlign: 'center', padding: '1rem' }}>
                <div className="stat-label" style={{ marginBottom: '0.5rem' }}>
                  Avg Battery Level
                </div>
                <div style={{ fontSize: '2rem', fontWeight: '600', color: '#f1c21b' }}>
                  {analytics?.average_battery_level?.toFixed(1) || 'N/A'}
                  {analytics?.average_battery_level && '%'}
                </div>
              </div>
            </Column>
          </Grid>
        </Tile>
      </Column>
      </Grid>
    </>
  );
}

// Made with Bob
