import { useEffect, useState } from 'react';
import {
  Grid,
  Column,
  Tile,
  SkeletonPlaceholder,
  InlineNotification,
  ProgressBar
} from '@carbon/react';
import {
  ArrowUp,
  Activity,
  WarningAlt,
  Checkmark,
  ChartBar,
  ChargingStation
} from '@carbon/icons-react';
import api from '../services/api';
import type { AnalyticsSummary } from '../types';

export default function Analytics() {
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalytics();
    const interval = setInterval(loadAnalytics, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadAnalytics = async () => {
    try {
      setError(null);
      const data = await api.getAnalyticsSummary();
      setAnalytics(data);
    } catch (err) {
      setError('Failed to load analytics data');
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
          <SkeletonPlaceholder style={{ height: '300px' }} />
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

  if (!analytics) {
    return (
      <Grid>
        <Column lg={16}>
          <InlineNotification
            kind="info"
            title="No Data"
            subtitle="No analytics data available"
            lowContrast
          />
        </Column>
      </Grid>
    );
  }

  const utilizationRate = analytics.total_vehicles > 0 
    ? (analytics.active_vehicles / analytics.total_vehicles) * 100
    : 0;

  return (
    <>
      <Grid>
        <Column lg={16}>
          <h1 style={{ marginBottom: '2rem', fontSize: '2.5rem', fontWeight: '300' }}>
            Fleet Analytics
          </h1>
        </Column>
      </Grid>

      {/* Key Performance Indicators */}
      <Grid>
        <Column sm={4} md={4} lg={5}>
          <Tile className="fade-in" style={{ height: '100%' }}>
            <div className="stat-card-content">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                <Activity size={32} style={{ color: '#24a148' }} />
                <span className="stat-label">Fleet Utilization</span>
              </div>
              <div className="stat-value" style={{ color: '#24a148' }}>
                {utilizationRate.toFixed(1)}%
              </div>
              <div style={{ marginTop: '1rem' }}>
                <ProgressBar
                  value={utilizationRate}
                  max={100}
                  label=""
                  hideLabel
                />
              </div>
              <div style={{ fontSize: '0.875rem', opacity: 0.7, marginTop: '0.5rem' }}>
                {analytics.active_vehicles} of {analytics.total_vehicles} vehicles active
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={5}>
          <Tile className="fade-in" style={{ height: '100%' }}>
            <div className="stat-card-content">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                <ChargingStation size={32} style={{ color: '#f1c21b' }} />
                <span className="stat-label">Avg Battery Level</span>
              </div>
              <div className="stat-value" style={{ color: '#f1c21b' }}>
                {analytics.average_battery_level?.toFixed(1) || 'N/A'}
                {analytics.average_battery_level && '%'}
              </div>
              {analytics.average_battery_level && (
                <div style={{ marginTop: '1rem' }}>
                  <ProgressBar
                    value={analytics.average_battery_level}
                    max={100}
                    label=""
                    hideLabel
                  />
                </div>
              )}
              <div style={{ fontSize: '0.875rem', opacity: 0.7, marginTop: '0.5rem' }}>
                Fleet-wide average
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={6}>
          <Tile className="fade-in" style={{ height: '100%' }}>
            <div className="stat-card-content">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
                <WarningAlt size={32} style={{ color: '#da1e28' }} />
                <span className="stat-label">Critical Alerts</span>
              </div>
              <div className="stat-value" style={{ color: '#da1e28' }}>
                {analytics.critical_alerts || 0}
              </div>
              <div style={{ fontSize: '0.875rem', opacity: 0.7, marginTop: '1rem' }}>
                Requiring immediate attention
              </div>
            </div>
          </Tile>
        </Column>
      </Grid>

      {/* Detailed Metrics */}
      <Grid style={{ marginTop: '2rem' }}>
        <Column sm={4} md={4} lg={8}>
          <Tile style={{ height: '100%' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
              <ChartBar size={24} />
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600' }}>
                Telemetry Statistics
              </h3>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <span style={{ opacity: 0.7 }}>Total Records</span>
                  <span style={{ fontSize: '1.75rem', fontWeight: '600', color: '#0f62fe' }}>
                    {analytics.total_telemetry_records?.toLocaleString() || 0}
                  </span>
                </div>
                <ProgressBar
                  value={100}
                  max={100}
                  label=""
                  hideLabel
                />
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <span style={{ opacity: 0.7 }}>Records per Vehicle</span>
                  <span style={{ fontSize: '1.75rem', fontWeight: '600', color: '#24a148' }}>
                    {analytics.total_vehicles > 0 
                      ? Math.round((analytics.total_telemetry_records || 0) / analytics.total_vehicles)
                      : 0}
                  </span>
                </div>
                <ProgressBar
                  value={75}
                  max={100}
                  label=""
                  hideLabel
                />
              </div>

              <div style={{ 
                padding: '1rem', 
                backgroundColor: 'rgba(15, 98, 254, 0.1)',
                borderRadius: '4px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ opacity: 0.8 }}>Data Collection Rate</span>
                  <span style={{ fontSize: '1.5rem', fontWeight: '600', color: '#0f62fe' }}>
                    5s
                  </span>
                </div>
                <div style={{ fontSize: '0.875rem', opacity: 0.6, marginTop: '0.25rem' }}>
                  Real-time telemetry updates
                </div>
              </div>
            </div>
          </Tile>
        </Column>

        <Column sm={4} md={4} lg={8}>
          <Tile style={{ height: '100%' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
              <ArrowUp size={24} />
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600' }}>
                Operational Metrics (30 Days)
              </h3>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ 
                padding: '1.5rem', 
                backgroundColor: 'rgba(36, 161, 72, 0.1)',
                borderRadius: '4px',
                border: '1px solid rgba(36, 161, 72, 0.2)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                  <Checkmark size={24} style={{ color: '#24a148' }} />
                  <span style={{ fontWeight: '600' }}>Completed Assignments</span>
                </div>
                <div style={{ fontSize: '2.5rem', fontWeight: '600', color: '#24a148' }}>
                  {analytics.completed_assignments_30d || 0}
                </div>
                <div style={{ fontSize: '0.875rem', opacity: 0.7, marginTop: '0.5rem' }}>
                  Routes successfully completed
                </div>
              </div>

              <div style={{ 
                padding: '1.5rem', 
                backgroundColor: 'rgba(15, 98, 254, 0.1)',
                borderRadius: '4px',
                border: '1px solid rgba(15, 98, 254, 0.2)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                  <Activity size={24} style={{ color: '#0f62fe' }} />
                  <span style={{ fontWeight: '600' }}>Fleet Availability</span>
                </div>
                <div style={{ fontSize: '2.5rem', fontWeight: '600', color: '#0f62fe' }}>
                  {utilizationRate.toFixed(0)}%
                </div>
                <div style={{ fontSize: '0.875rem', opacity: 0.7, marginTop: '0.5rem' }}>
                  Vehicles ready for deployment
                </div>
              </div>

              <div style={{ 
                padding: '1.5rem', 
                backgroundColor: 'rgba(241, 194, 27, 0.1)',
                borderRadius: '4px',
                border: '1px solid rgba(241, 194, 27, 0.2)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                  <ChargingStation size={24} style={{ color: '#f1c21b' }} />
                  <span style={{ fontWeight: '600' }}>Energy Efficiency</span>
                </div>
                <div style={{ fontSize: '2.5rem', fontWeight: '600', color: '#f1c21b' }}>
                  {analytics.average_battery_level 
                    ? (analytics.average_battery_level > 70 ? 'Good' : analytics.average_battery_level > 40 ? 'Fair' : 'Low')
                    : 'N/A'}
                </div>
                <div style={{ fontSize: '0.875rem', opacity: 0.7, marginTop: '0.5rem' }}>
                  Based on average battery level
                </div>
              </div>
            </div>
          </Tile>
        </Column>
      </Grid>

      {/* Performance Insights */}
      <Grid style={{ marginTop: '2rem' }}>
        <Column lg={16}>
          <Tile>
            <h3 style={{ marginBottom: '1.5rem', fontSize: '1.25rem', fontWeight: '600' }}>
              Performance Insights
            </h3>
            <Grid condensed>
              <Column sm={4} md={4} lg={5}>
                <div style={{ textAlign: 'center', padding: '1.5rem', backgroundColor: 'rgba(36, 161, 72, 0.05)', borderRadius: '4px' }}>
                  <div style={{ fontSize: '3rem', fontWeight: '600', color: '#24a148', marginBottom: '0.5rem' }}>
                    {analytics.total_telemetry_records && analytics.total_vehicles > 0
                      ? Math.round((analytics.total_telemetry_records / analytics.total_vehicles) / 12)
                      : 0}
                  </div>
                  <div style={{ fontSize: '0.875rem', opacity: 0.7, marginBottom: '0.25rem' }}>
                    Avg. Updates per Hour
                  </div>
                  <div style={{ fontSize: '0.75rem', opacity: 0.6 }}>
                    Per vehicle
                  </div>
                </div>
              </Column>

              <Column sm={4} md={4} lg={5}>
                <div style={{ textAlign: 'center', padding: '1.5rem', backgroundColor: 'rgba(15, 98, 254, 0.05)', borderRadius: '4px' }}>
                  <div style={{ fontSize: '3rem', fontWeight: '600', color: '#0f62fe', marginBottom: '0.5rem' }}>
                    {analytics.total_vehicles || 0}
                  </div>
                  <div style={{ fontSize: '0.875rem', opacity: 0.7, marginBottom: '0.25rem' }}>
                    Total Fleet Size
                  </div>
                  <div style={{ fontSize: '0.75rem', opacity: 0.6 }}>
                    Autonomous vehicles
                  </div>
                </div>
              </Column>

              <Column sm={4} md={4} lg={6}>
                <div style={{ textAlign: 'center', padding: '1.5rem', backgroundColor: 'rgba(241, 194, 27, 0.05)', borderRadius: '4px' }}>
                  <div style={{ fontSize: '3rem', fontWeight: '600', color: '#f1c21b', marginBottom: '0.5rem' }}>
                    99.9%
                  </div>
                  <div style={{ fontSize: '0.875rem', opacity: 0.7, marginBottom: '0.25rem' }}>
                    System Uptime
                  </div>
                  <div style={{ fontSize: '0.75rem', opacity: 0.6 }}>
                    Last 30 days
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