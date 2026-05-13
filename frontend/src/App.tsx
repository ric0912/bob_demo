import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import {
  Header,
  HeaderContainer,
  HeaderName,
  HeaderNavigation,
  HeaderMenuItem,
  HeaderGlobalBar,
  HeaderGlobalAction,
  SkipToContent,
  Content,
  Theme
} from '@carbon/react';
import { Dashboard, Activity, Analytics, Notification } from '@carbon/icons-react';
import DashboardPage from './components/Dashboard';
import VehicleList from './components/VehicleList';
import TelemetryStream from './components/TelemetryStream';
import AnalyticsPage from './components/Analytics';

function AppContent() {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <Theme theme="g10">
      <HeaderContainer
        render={() => (
          <>
            <Header aria-label="Fleet Management Platform">
              <SkipToContent />
              <HeaderName prefix="IBM" onClick={() => navigate('/')}>
                Fleet Management
              </HeaderName>
              <HeaderNavigation aria-label="Fleet Management">
                <HeaderMenuItem
                  onClick={() => navigate('/')}
                  isActive={isActive('/')}
                >
                  Dashboard
                </HeaderMenuItem>
                <HeaderMenuItem
                  onClick={() => navigate('/vehicles')}
                  isActive={isActive('/vehicles')}
                >
                  Vehicles
                </HeaderMenuItem>
                <HeaderMenuItem
                  onClick={() => navigate('/telemetry')}
                  isActive={isActive('/telemetry')}
                >
                  Telemetry
                </HeaderMenuItem>
                <HeaderMenuItem
                  onClick={() => navigate('/analytics')}
                  isActive={isActive('/analytics')}
                >
                  Analytics
                </HeaderMenuItem>
              </HeaderNavigation>
              <HeaderGlobalBar>
                <HeaderGlobalAction
                  aria-label="Notifications"
                  tooltipAlignment="end"
                >
                  <Notification size={20} />
                </HeaderGlobalAction>
              </HeaderGlobalBar>
            </Header>
            <Content className="main-content">
              <Routes>
                <Route path="/" element={<DashboardPage />} />
                <Route path="/vehicles" element={<VehicleList />} />
                <Route path="/telemetry" element={<TelemetryStream />} />
                <Route path="/analytics" element={<AnalyticsPage />} />
              </Routes>
            </Content>
          </>
        )}
      />
    </Theme>
  );
}

function App() {
  return (
    <Router>
      <div className="app">
        <AppContent />
      </div>
    </Router>
  );
}

export default App;

// Made with Bob
