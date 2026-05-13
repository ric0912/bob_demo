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
- **Orchestration**: Kubernetes (IBM Cloud Kubernetes Service) / IBM Code Engine
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions with automated deployment
- **Monitoring**: Prometheus + Grafana (optional)
- **Cloud Platform**: IBM Cloud (IKS & Code Engine)

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
        I[IBM Cloud IKS / Code Engine]
        J[IBM Cloud MySQL]
        K[Container Registry]
    end
    
    subgraph "CI/CD"
        L[GitHub Actions]
        M[Automated Deployment]
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
    L -.->|Builds & Pushes| K
    M -.->|Deploys| I
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

### Phase 3: Kubernetes/Code Engine Configuration

#### Option A: Kubernetes Deployment
1. Create namespace and resource quotas
2. Set up ConfigMaps and Secrets
3. Create MySQL StatefulSet with persistent storage
4. Deploy backend as Deployment with multiple replicas
5. Deploy frontend as Deployment
6. Configure Services and Ingress
7. Add Horizontal Pod Autoscaler

#### Option B: IBM Code Engine Deployment (Recommended for Simplicity)
1. Create Code Engine project
2. Set up IBM Cloud Databases for MySQL
3. Create secrets and configmaps in Code Engine
4. Deploy backend application with auto-scaling
5. Deploy frontend application
6. Configure custom domains (optional)
7. Set up monitoring and logging

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

### Phase 5: CI/CD Pipelines with GitHub Actions

1. **Backend CI Pipeline** (`.github/workflows/backend-ci.yml`):
   - Run linting and code quality checks (flake8, black)
   - Execute unit tests with pytest
   - Generate code coverage reports
   - Build Docker image
   - Push to IBM Container Registry
   - Run security scans (bandit, safety)

2. **Frontend CI Pipeline** (`.github/workflows/frontend-ci.yml`):
   - Run linting and type checking (ESLint, TypeScript)
   - Execute unit tests with Vitest
   - Build production bundle
   - Build Docker image
   - Push to IBM Container Registry
   - Run Lighthouse CI for performance

3. **Terraform Pipeline** (`.github/workflows/terraform.yml`):
   - Validate Terraform configuration
   - Run `terraform plan`
   - Apply on approval (for main branch)
   - Manage IBM Cloud infrastructure

4. **Code Engine Deployment Pipeline** (`.github/workflows/deploy-code-engine.yml`):
   - Authenticate with IBM Cloud
   - Select Code Engine project
   - Deploy backend application with new image
   - Deploy frontend application with new image
   - Run smoke tests after deployment
   - Send deployment notifications (Slack/Email)
   - Automatic rollback on failure

5. **Multi-Environment Strategy**:
   - **Dev**: Auto-deploy on push to `main`
   - **Staging**: Deploy on approval after dev success
   - **Production**: Deploy on approval with manual gate
   - Environment-specific secrets and configurations
   - Blue-green deployment for zero downtime

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

## IBM Code Engine Deployment Guide

### Why Code Engine?

IBM Code Engine offers several advantages over traditional Kubernetes:

1. **Serverless Architecture**: No cluster management overhead
2. **Cost Efficiency**: Pay only for actual resource usage, scales to zero
3. **Faster Deployment**: Deploy in seconds vs minutes
4. **Built-in CI/CD**: Native GitHub integration
5. **Auto-scaling**: Automatic horizontal scaling based on load
6. **Simplified Operations**: No need to manage nodes, pods, or infrastructure

### Code Engine vs Kubernetes Comparison

| Feature | Kubernetes (IKS) | Code Engine |
|---------|------------------|-------------|
| Setup Time | 30-60 minutes | 5-10 minutes |
| Management | Manual cluster management | Fully managed |
| Scaling | Manual HPA configuration | Automatic |
| Cost | Fixed cluster cost | Pay-per-use |
| Complexity | High (K8s expertise needed) | Low (simple CLI/UI) |
| Best For | Large-scale, complex apps | Microservices, APIs |

### Code Engine Deployment Steps

#### 1. Initial Setup (One-time)

```bash
# Install IBM Cloud CLI and plugins
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
ibmcloud plugin install code-engine
ibmcloud plugin install container-registry

# Login and setup
ibmcloud login --sso
ibmcloud target -r us-south -g default

# Create Code Engine project
ibmcloud ce project create --name fleet-management
ibmcloud ce project select --name fleet-management

# Create Container Registry namespace
ibmcloud cr namespace-add fleet-management
```

#### 2. Database Setup

**Important**: Code Engine doesn't host databases. Choose one of these options:

##### Option 0: In-Memory SQLite (No External Database - Recommended for Demo)

**Perfect for quick demos and testing!** No external database setup required.

```bash
# Create secrets for SQLite mode
ibmcloud ce secret create --name app-config \
  --from-literal DATABASE_URL="sqlite:///./fleet_management.db" \
  --from-literal USE_SQLITE="true" \
  --from-literal GENERATE_DUMMY_DATA="true" \
  --from-literal SECRET_KEY="demo-secret-key"
```

**Pros**:
- ✅ Zero setup time
- ✅ No cost
- ✅ Auto-generates dummy data
- ✅ Perfect for demos

**Cons**:
- ❌ Data lost on restart
- ❌ Not suitable for production
- ❌ Single instance only (no scaling)

**Cost**: $0 | **Setup Time**: 0 minutes

##### Option A: IBM Cloud Databases for MySQL (Recommended)

```bash
# Create IBM Cloud Databases for MySQL
ibmcloud resource service-instance-create fleet-mysql \
  databases-for-mysql standard us-south \
  -p '{"members_memory_allocation_mb": "3072", "members_disk_allocation_mb": "20480"}'

# Create service credentials
ibmcloud resource service-key-create fleet-mysql-key \
  --instance-name fleet-mysql

# Get connection details
ibmcloud resource service-key fleet-mysql-key --output json
```

**Cost**: ~$100-300/month | **Setup Time**: 10-15 minutes

##### Option B: PlanetScale (Free Tier for Development)

1. Sign up at https://planetscale.com
2. Create a new database
3. Get connection string from dashboard
4. Use the connection string in your Code Engine secrets

**Cost**: Free (5GB storage) | **Setup Time**: 5 minutes

##### Option C: Other Cloud Providers

- **AWS RDS MySQL**: `aws rds create-db-instance`
- **Google Cloud SQL**: `gcloud sql instances create`
- **Azure MySQL**: `az mysql server create`
- **DigitalOcean**: Via web console or API

##### Option D: Self-Hosted (Development Only)

```bash
# Deploy MySQL on IBM Cloud Virtual Server
ibmcloud is instance-create mysql-server \
  --image ibm-ubuntu-20-04-minimal-amd64-1 \
  --profile bx2-2x8

# SSH and install MySQL
ssh root@<instance-ip>
apt update && apt install mysql-server -y
```

**Not recommended for production** - requires manual management and backups.

#### 3. Application Deployment

```bash
# Build and push images
docker build -t us.icr.io/fleet-management/backend:latest ./backend
docker build -t us.icr.io/fleet-management/frontend:latest ./frontend
docker push us.icr.io/fleet-management/backend:latest
docker push us.icr.io/fleet-management/frontend:latest

# Create secrets
ibmcloud ce secret create --name mysql-credentials \
  --from-literal DATABASE_URL="mysql+pymysql://user:pass@host:port/fleet_management" \
  --from-literal SECRET_KEY="your-secret-key"

# Deploy backend
ibmcloud ce application create --name fleet-backend \
  --image us.icr.io/fleet-management/backend:latest \
  --registry-secret icr-secret \
  --env-from-secret mysql-credentials \
  --port 8000 \
  --min-scale 1 \
  --max-scale 10 \
  --cpu 0.5 \
  --memory 1G

# Deploy frontend
ibmcloud ce application create --name fleet-frontend \
  --image us.icr.io/fleet-management/frontend:latest \
  --registry-secret icr-secret \
  --port 80 \
  --min-scale 1 \
  --max-scale 5 \
  --cpu 0.25 \
  --memory 512M
```

### GitHub Actions Workflows for Code Engine

#### Backend CI/CD Workflow

Create `.github/workflows/backend-ci-cd.yml`:

```yaml
name: Backend CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'backend/**'
  pull_request:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app tests/
      - name: Lint
        run: |
          cd backend
          flake8 app/
          black --check app/

  build-and-deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install IBM Cloud CLI
        run: |
          curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
          ibmcloud plugin install code-engine
          ibmcloud plugin install container-registry
      - name: Authenticate
        run: |
          ibmcloud login --apikey ${{ secrets.IBM_CLOUD_API_KEY }} -r us-south
          ibmcloud cr login
      - name: Build and Push
        run: |
          docker build -t us.icr.io/fleet-management/backend:${{ github.sha }} ./backend
          docker push us.icr.io/fleet-management/backend:${{ github.sha }}
      - name: Deploy to Code Engine
        run: |
          ibmcloud ce project select --name fleet-management
          ibmcloud ce application update --name fleet-backend \
            --image us.icr.io/fleet-management/backend:${{ github.sha }}
```

#### Frontend CI/CD Workflow

Create `.github/workflows/frontend-ci-cd.yml`:

```yaml
name: Frontend CI/CD

on:
  push:
    branches: [main, develop]
    paths:
      - 'frontend/**'
  pull_request:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run tests
        run: |
          cd frontend
          npm test
      - name: Lint
        run: |
          cd frontend
          npm run lint

  build-and-deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install IBM Cloud CLI
        run: |
          curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
          ibmcloud plugin install code-engine
          ibmcloud plugin install container-registry
      - name: Authenticate
        run: |
          ibmcloud login --apikey ${{ secrets.IBM_CLOUD_API_KEY }} -r us-south
          ibmcloud cr login
      - name: Build and Push
        run: |
          docker build -t us.icr.io/fleet-management/frontend:${{ github.sha }} ./frontend
          docker push us.icr.io/fleet-management/frontend:${{ github.sha }}
      - name: Deploy to Code Engine
        run: |
          ibmcloud ce project select --name fleet-management
          ibmcloud ce application update --name fleet-frontend \
            --image us.icr.io/fleet-management/frontend:${{ github.sha }}
```

### Monitoring and Management

```bash
# View applications
ibmcloud ce application list

# View logs
ibmcloud ce application logs --name fleet-backend --follow

# Check application status
ibmcloud ce application get --name fleet-backend

# View revisions
ibmcloud ce revision list --application fleet-backend

# Scale application
ibmcloud ce application update --name fleet-backend --min-scale 2 --max-scale 20

# Rollback to previous version
ibmcloud ce application update --name fleet-backend \
  --image us.icr.io/fleet-management/backend:previous-sha
```


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

### IBM Cloud & Code Engine
- `IBM_CLOUD_API_KEY` - IBM Cloud API key with Code Engine and Container Registry permissions
- `IBM_CLOUD_REGION` - IBM Cloud region (e.g., `us-south`, `eu-de`, `jp-tok`)
- `IBM_CR_NAMESPACE` - Container Registry namespace
- `CODE_ENGINE_PROJECT` - Code Engine project name (e.g., `fleet-management`)

### Database Configuration
- `DATABASE_URL` - Full MySQL connection string
- `MYSQL_ROOT_PASSWORD` - MySQL root password
- `MYSQL_PASSWORD` - Application MySQL user password
- `DB_HOST` - Database host (for Code Engine: IBM Cloud Databases endpoint)
- `DB_PORT` - Database port (default: 3306)
- `DB_NAME` - Database name (default: `fleet_management`)
- `DB_USER` - Database username

### Application Secrets
- `SECRET_KEY` - Application secret key for JWT/sessions
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)

### Deployment Configuration
- `BACKEND_APP_NAME` - Backend application name in Code Engine (default: `fleet-backend`)
- `FRONTEND_APP_NAME` - Frontend application name in Code Engine (default: `fleet-frontend`)
- `BACKEND_MIN_SCALE` - Minimum backend instances (default: 1)
- `BACKEND_MAX_SCALE` - Maximum backend instances (default: 10)
- `FRONTEND_MIN_SCALE` - Minimum frontend instances (default: 1)
- `FRONTEND_MAX_SCALE` - Maximum frontend instances (default: 5)

### Optional Notifications
- `SLACK_WEBHOOK_URL` - Slack webhook for deployment notifications
- `NOTIFICATION_EMAIL` - Email for deployment notifications

## Success Criteria

### Functional Requirements
✅ All API endpoints working correctly
✅ Real-time telemetry streaming functional
✅ Frontend dashboard displaying data
✅ Database operations performing efficiently
✅ Event queue processing messages

### DevOps Requirements
✅ Application runs locally via Docker Compose
✅ Kubernetes manifests deploy successfully (Option A)
✅ Code Engine deployment working (Option B - Recommended)
✅ Terraform provisions IBM Cloud infrastructure
✅ CI/CD pipelines execute without errors
✅ Automated tests pass in GitHub Actions
✅ Health checks respond correctly
✅ Monitoring metrics available
✅ Auto-scaling configured and tested
✅ Zero-downtime deployments achieved

### CI/CD Requirements
✅ Backend CI pipeline runs on every push
✅ Frontend CI pipeline runs on every push
✅ Automated deployment to Code Engine on main branch
✅ Deployment notifications working
✅ Rollback mechanism tested
✅ Multi-environment deployment (dev/staging/prod)
✅ GitHub secrets properly configured
✅ Container images pushed to IBM Container Registry

### Documentation Requirements
✅ README with setup instructions
✅ Architecture documentation
✅ API documentation
✅ Deployment guide (Kubernetes & Code Engine)
✅ CI/CD pipeline documentation
✅ Troubleshooting guide
✅ GitHub Actions workflow examples

## Timeline Estimate

- **Phase 1**: Local Development Setup - 2-3 hours
- **Phase 2**: Containerization - 1 hour
- **Phase 3**: Kubernetes/Code Engine Configuration - 1-2 hours
- **Phase 4**: Infrastructure as Code - 2-3 hours
- **Phase 5**: CI/CD Pipelines with GitHub Actions - 2-3 hours
- **Phase 6**: Monitoring & Observability - 1 hour
- **Phase 7**: Documentation & Scripts - 1-2 hours

**Total Estimated Time**: 10-15 hours

### Code Engine Deployment Timeline (Alternative)
- **Phase 1**: Local Development Setup - 2-3 hours
- **Phase 2**: Containerization - 1 hour
- **Phase 3**: Code Engine Setup & Deployment - 1 hour
- **Phase 4**: GitHub Actions CI/CD Setup - 1-2 hours
- **Phase 5**: Testing & Monitoring - 1 hour
- **Phase 6**: Documentation - 1 hour

**Code Engine Total**: 7-9 hours (Faster than Kubernetes)

## Next Steps

1. Review and approve this plan
2. Switch to Code mode to begin implementation
3. Start with Phase 1: Local Development Setup
4. Iterate through each phase sequentially
5. Test thoroughly at each stage
6. Deploy to IBM Cloud for final demonstration