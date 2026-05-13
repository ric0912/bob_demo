# Fleet Management Platform - DevOps Demo Project Plan

## Project Overview

A full-stack autonomous vehicle fleet management platform demonstrating comprehensive DevOps practices including Infrastructure as Code, CI/CD pipelines, containerization, and cloud deployment on IBM Cloud.

## Technology Stack

### Application Layer
- **Frontend**: React 18 + Vite + TypeScript
- **Backend**: FastAPI (Python 3.11+)
- **Database**: MySQL 8.0
- **Event System**: Custom In-Memory Event Queue (Python asyncio)

### DevOps Tools
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (IBM Cloud Kubernetes Service)
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana (optional)
- **Cloud Platform**: IBM Cloud

## Project Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[React Dashboard]
    end
    
    subgraph "API Gateway"
        B[FastAPI Backend]
    end
    
    subgraph "Services"
        C[Vehicle Service]
        D[Telemetry Service]
        E[Fleet Service]
        F[Analytics Service]
    end
    
    subgraph "Data Layer"
        G[MySQL Database]
        H[Event Queue]
    end
    
    subgraph "Infrastructure"
        I[IBM Cloud IKS]
        J[IBM Cloud MySQL]
        K[Container Registry]
    end
    
    A -->|REST API| B
    B --> C
    B --> D
    B --> E
    B --> F
    C --> G
    D --> G
    E --> G
    F --> G
    C --> H
    D --> H
    E --> H
    
    I -.->|Hosts| A
    I -.->|Hosts| B
    J -.->|Managed DB| G
    K -.->|Images| I
```

## Project Structure

```
fleet-management-platform/
├── README.md
├── PLAN.md
├── .gitignore
├── docker-compose.yml
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── vehicles.py
│   │   │   ├── telemetry.py
│   │   │   ├── fleet.py
│   │   │   └── analytics.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── vehicle.py
│   │   │   ├── telemetry.py
│   │   │   └── fleet.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── vehicle.py
│   │   │   ├── telemetry.py
│   │   │   └── fleet.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── vehicle_service.py
│   │   │   ├── telemetry_service.py
│   │   │   └── fleet_service.py
│   │   └── events/
│   │       ├── __init__.py
│   │       ├── event_queue.py
│   │       └── event_handlers.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_vehicles.py
│   │   └── test_telemetry.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── VehicleList.tsx
│   │   │   ├── VehicleMap.tsx
│   │   │   ├── TelemetryChart.tsx
│   │   │   └── FleetStats.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── websocket.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   └── utils/
│   │       └── helpers.ts
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── .env.example
│
├── infrastructure/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── providers.tf
│   ├── terraform.tfvars.example
│   ├── modules/
│   │   ├── kubernetes/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── database/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── networking/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   └── container-registry/
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       └── outputs.tf
│   └── environments/
│       ├── dev/
│       │   └── terraform.tfvars
│       ├── staging/
│       │   └── terraform.tfvars
│       └── prod/
│           └── terraform.tfvars
│
├── kubernetes/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── mysql-statefulset.yaml
│   ├── mysql-service.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       ├── frontend-ci.yml
│       ├── terraform-plan.yml
│       ├── terraform-apply.yml
│       └── deploy.yml
│
├── scripts/
│   ├── setup-local.sh
│   ├── deploy.sh
│   ├── init-db.sql
│   └── seed-data.sql
│
└── docs/
    ├── ARCHITECTURE.md
    ├── DEPLOYMENT.md
    ├── API.md
    └── DEVELOPMENT.md
```

## Core Features

### 1. Vehicle Management
- Register and manage autonomous vehicles
- Track vehicle status (active, idle, maintenance, offline)
- Vehicle metadata (make, model, year, VIN, license plate)
- Vehicle location tracking

### 2. Real-time Telemetry
- GPS coordinates and speed
- Battery level and charging status
- Sensor health (LiDAR, cameras, radar)
- System diagnostics
- Real-time event streaming

### 3. Fleet Operations
- Fleet overview dashboard
- Active vehicle count and status
- Route assignments
- Maintenance scheduling
- Alert management

### 4. Analytics
- Historical data analysis
- Performance metrics
- Usage statistics
- Trend visualization
- Custom reports

## Database Schema

### Tables

**vehicles**
```sql
CREATE TABLE vehicles (
    id VARCHAR(36) PRIMARY KEY,
    vin VARCHAR(17) UNIQUE NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    license_plate VARCHAR(20),
    status ENUM('active', 'idle', 'maintenance', 'offline') DEFAULT 'idle',
    battery_capacity DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**telemetry**
```sql
CREATE TABLE telemetry (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id VARCHAR(36) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    speed DECIMAL(5,2),
    battery_level DECIMAL(5,2),
    heading DECIMAL(5,2),
    odometer DECIMAL(10,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    INDEX idx_vehicle_timestamp (vehicle_id, timestamp)
);
```

**fleet_assignments**
```sql
CREATE TABLE fleet_assignments (
    id VARCHAR(36) PRIMARY KEY,
    vehicle_id VARCHAR(36) NOT NULL,
    route_id VARCHAR(36),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    status ENUM('assigned', 'in_progress', 'completed', 'cancelled') DEFAULT 'assigned',
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);
```

**alerts**
```sql
CREATE TABLE alerts (
    id VARCHAR(36) PRIMARY KEY,
    vehicle_id VARCHAR(36) NOT NULL,
    alert_type ENUM('battery_low', 'maintenance_required', 'sensor_failure', 'system_error') NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    message TEXT,
    acknowledged BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
    INDEX idx_vehicle_severity (vehicle_id, severity)
);
```

## API Endpoints

### Vehicle Management
- `GET /api/v1/vehicles` - List all vehicles
- `POST /api/v1/vehicles` - Register new vehicle
- `GET /api/v1/vehicles/{id}` - Get vehicle details
- `PUT /api/v1/vehicles/{id}` - Update vehicle
- `DELETE /api/v1/vehicles/{id}` - Remove vehicle
- `GET /api/v1/vehicles/{id}/status` - Get vehicle status

### Telemetry
- `GET /api/v1/telemetry` - Get telemetry data (with filters)
- `POST /api/v1/telemetry` - Submit telemetry data
- `GET /api/v1/telemetry/vehicle/{id}` - Get vehicle telemetry history
- `GET /api/v1/telemetry/latest` - Get latest telemetry for all vehicles
- `WS /api/v1/telemetry/stream` - WebSocket for real-time telemetry

### Fleet Operations
- `GET /api/v1/fleet/overview` - Fleet statistics
- `GET /api/v1/fleet/assignments` - List assignments
- `POST /api/v1/fleet/assignments` - Create assignment
- `PUT /api/v1/fleet/assignments/{id}` - Update assignment
- `GET /api/v1/fleet/alerts` - List alerts
- `POST /api/v1/fleet/alerts/{id}/acknowledge` - Acknowledge alert

### Analytics
- `GET /api/v1/analytics/summary` - Overall statistics
- `GET /api/v1/analytics/vehicle/{id}` - Vehicle-specific analytics
- `GET /api/v1/analytics/performance` - Performance metrics
- `GET /api/v1/analytics/trends` - Trend analysis

### Health & Monitoring
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics
- `GET /api/v1/status` - System status

## DevOps Implementation Plan

### Phase 1: Local Development Setup
1. Create project structure
2. Set up backend FastAPI application
3. Implement MySQL database models
4. Create in-memory event queue
5. Build frontend React application
6. Configure Docker Compose for local development
7. Add seed data and test scripts

### Phase 2: Containerization
1. Create optimized Dockerfiles for backend and frontend
2. Set up multi-stage builds
3. Configure Docker Compose with all services
4. Add health checks and restart policies
5. Create development and production configurations

### Phase 3: Kubernetes Configuration
1. Create namespace and resource quotas
2. Set up ConfigMaps and Secrets
3. Create MySQL StatefulSet with persistent storage
4. Deploy backend as Deployment with multiple replicas
5. Deploy frontend as Deployment
6. Configure Services and Ingress
7. Add Horizontal Pod Autoscaler

### Phase 4: Infrastructure as Code (Terraform)
1. Set up Terraform project structure
2. Create IBM Cloud provider configuration
3. Build modules for:
   - IBM Cloud Kubernetes Service (IKS)
   - IBM Cloud Databases for MySQL
   - VPC and networking
   - Container Registry
   - IAM roles and policies
4. Create environment-specific configurations (dev/staging/prod)
5. Set up remote state management
6. Add outputs for CI/CD integration

### Phase 5: CI/CD Pipelines
1. Backend CI pipeline:
   - Run linting and code quality checks
   - Execute unit tests
   - Build Docker image
   - Push to IBM Container Registry
   - Run security scans
2. Frontend CI pipeline:
   - Run linting and type checking
   - Execute unit tests
   - Build production bundle
   - Build Docker image
   - Push to IBM Container Registry
3. Terraform pipeline:
   - Validate configuration
   - Run terraform plan
   - Apply on approval (for main branch)
4. Deployment pipeline:
   - Deploy to dev environment automatically
   - Deploy to staging on approval
   - Deploy to production on approval
   - Run smoke tests after deployment

### Phase 6: Monitoring & Observability
1. Add Prometheus metrics endpoints
2. Create Grafana dashboards
3. Set up logging aggregation
4. Configure alerting rules
5. Add health check endpoints
6. Implement distributed tracing (optional)

### Phase 7: Documentation & Scripts
1. Create comprehensive README
2. Write architecture documentation
3. Document API endpoints
4. Create deployment guides
5. Add troubleshooting guides
6. Create helper scripts for common tasks

## Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/fleet_management
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fleet_management
DB_USER=fleetuser
DB_PASSWORD=fleetpass

# Application
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# IBM Cloud (Production)
IBM_CLOUD_API_KEY=your-api-key
IBM_CLOUD_REGION=us-south
```

### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_ENVIRONMENT=development
```

### Terraform (terraform.tfvars)
```hcl
ibmcloud_api_key = "your-api-key"
region           = "us-south"
resource_group   = "default"
cluster_name     = "fleet-mgmt-cluster"
mysql_plan       = "standard"
environment      = "dev"
```

## GitHub Secrets Required

- `IBM_CLOUD_API_KEY` - IBM Cloud API key for deployment
- `IBM_CLOUD_REGION` - IBM Cloud region
- `IBM_CR_NAMESPACE` - Container Registry namespace
- `MYSQL_ROOT_PASSWORD` - MySQL root password
- `MYSQL_PASSWORD` - Application MySQL password
- `SECRET_KEY` - Application secret key

## Success Criteria

### Functional Requirements
✅ All API endpoints working correctly
✅ Real-time telemetry streaming functional
✅ Frontend dashboard displaying data
✅ Database operations performing efficiently
✅ Event queue processing messages

### DevOps Requirements
✅ Application runs locally via Docker Compose
✅ Kubernetes manifests deploy successfully
✅ Terraform provisions IBM Cloud infrastructure
✅ CI/CD pipelines execute without errors
✅ Automated tests pass
✅ Health checks respond correctly
✅ Monitoring metrics available

### Documentation Requirements
✅ README with setup instructions
✅ Architecture documentation
✅ API documentation
✅ Deployment guide
✅ Troubleshooting guide

## Timeline Estimate

- **Phase 1**: Local Development Setup - 2-3 hours
- **Phase 2**: Containerization - 1 hour
- **Phase 3**: Kubernetes Configuration - 1-2 hours
- **Phase 4**: Infrastructure as Code - 2-3 hours
- **Phase 5**: CI/CD Pipelines - 2 hours
- **Phase 6**: Monitoring & Observability - 1 hour
- **Phase 7**: Documentation & Scripts - 1 hour

**Total Estimated Time**: 10-13 hours

## Next Steps

1. Review and approve this plan
2. Switch to Code mode to begin implementation
3. Start with Phase 1: Local Development Setup
4. Iterate through each phase sequentially
5. Test thoroughly at each stage
6. Deploy to IBM Cloud for final demonstration