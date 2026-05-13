# Fleet Management Platform

A comprehensive DevOps demonstration project showcasing a full-stack autonomous vehicle fleet management platform with complete CI/CD pipeline, Infrastructure as Code, and cloud deployment on IBM Cloud.

## 🚀 Project Overview

This project demonstrates modern DevOps practices through a real-world autonomous vehicle fleet management application, featuring:

- **Full-Stack Application**: React frontend + FastAPI backend
- **Database**: MySQL 8.0
- **Event-Driven Architecture**: Custom in-memory event queue
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes on IBM Cloud / IBM Code Engine
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions with automated deployment
- **Monitoring**: Health checks and metrics endpoints

## 📋 Features

### Application Features
- **Vehicle Management**: Register, track, and manage autonomous vehicles
- **Real-time Telemetry**: GPS tracking, battery monitoring, sensor data
- **Fleet Operations**: Assignment management, route planning, alerts
- **Analytics**: Performance metrics, trends, and reporting

### DevOps Features
- ✅ Multi-stage Docker builds
- ✅ Docker Compose for local development
- ✅ Kubernetes manifests for production deployment
- ✅ Terraform modules for IBM Cloud infrastructure
- ✅ Automated CI/CD pipelines
- ✅ Health checks and monitoring endpoints
- ✅ Multi-environment support (dev/staging/prod)

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│ MySQL  │ │  Event   │
│   DB   │ │  Queue   │
└────────┘ └──────────┘
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: MySQL 8.0 with SQLAlchemy ORM
- **Validation**: Pydantic
- **Event System**: Custom asyncio-based event queue
- **Testing**: pytest

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Language**: TypeScript
- **HTTP Client**: Axios

### DevOps
- **Containerization**: Docker
- **Orchestration**: Kubernetes / IBM Code Engine
- **IaC**: Terraform
- **CI/CD**: GitHub Actions
- **Cloud**: IBM Cloud (IKS & Code Engine)

## 📦 Project Structure

```
fleet-management-platform/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── events/         # Event queue system
│   │   └── main.py         # Application entry point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── infrastructure/         # Terraform IaC
│   ├── modules/
│   └── environments/
├── kubernetes/            # K8s manifests
├── .github/workflows/     # CI/CD pipelines
├── scripts/              # Helper scripts
└── docker-compose.yml    # Local development
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- MySQL 8.0 (or use Docker)
- Terraform (for infrastructure)
- IBM Cloud CLI (for deployment)

### Local Development with Docker Compose

1. **Clone the repository**
```bash
git clone <repository-url>
cd fleet-management-platform
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- MySQL: localhost:3306

4. **View logs**
```bash
docker-compose logs -f
```

5. **Stop services**
```bash
docker-compose down
```

### Manual Setup (Without Docker)

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Initialize database**
```bash
mysql -u root -p < ../scripts/init-db.sql
```

5. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API URL
```

3. **Run development server**
```bash
npm run dev
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/fleet_management
SECRET_KEY=your-secret-key
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### Frontend (.env)
```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## 📊 API Endpoints

### Health & Monitoring
- `GET /health` - Health check
- `GET /ready` - Readiness check
- `GET /live` - Liveness check
- `GET /metrics` - Prometheus metrics

### Vehicles
- `GET /api/v1/vehicles` - List all vehicles
- `POST /api/v1/vehicles` - Register new vehicle
- `GET /api/v1/vehicles/{id}` - Get vehicle details
- `PUT /api/v1/vehicles/{id}` - Update vehicle
- `DELETE /api/v1/vehicles/{id}` - Delete vehicle

### Telemetry
- `GET /api/v1/telemetry` - List telemetry data
- `POST /api/v1/telemetry` - Submit telemetry
- `GET /api/v1/telemetry/vehicle/{id}` - Get vehicle telemetry
- `GET /api/v1/telemetry/latest` - Latest telemetry for all vehicles

### Fleet Operations
- `GET /api/v1/fleet/overview` - Fleet statistics
- `GET /api/v1/fleet/assignments` - List assignments
- `POST /api/v1/fleet/assignments` - Create assignment
- `PUT /api/v1/fleet/assignments/{id}` - Update assignment
- `GET /api/v1/fleet/alerts` - List alerts
- `POST /api/v1/fleet/alerts/{id}/acknowledge` - Acknowledge alert

### Analytics
- `GET /api/v1/analytics/summary` - Overall statistics
- `GET /api/v1/analytics/vehicle/{id}` - Vehicle analytics
- `GET /api/v1/analytics/performance` - Performance metrics
- `GET /api/v1/analytics/trends` - Trend analysis

## 🐳 Docker Commands

### Build images
```bash
docker-compose build
```

### Start services
```bash
docker-compose up -d
```

### View logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Execute commands in containers
```bash
docker-compose exec backend bash
docker-compose exec mysql mysql -u fleetuser -p fleet_management
```

### Clean up
```bash
docker-compose down -v  # Remove volumes
```

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes
```bash
kubectl apply -f kubernetes/
```

### Check deployment status
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

### View logs
```bash
kubectl logs -f deployment/fleet-backend
```

## 🚀 IBM Code Engine Deployment

IBM Code Engine is a fully managed, serverless platform that runs containerized workloads without the need to manage Kubernetes clusters. It provides automatic scaling, built-in CI/CD, and pay-per-use pricing.

### Prerequisites
- IBM Cloud account
- IBM Cloud CLI installed
- Code Engine plugin: `ibmcloud plugin install code-engine`

### Database Hosting Options

**Important**: Code Engine is serverless and doesn't include database hosting. You need to use an external MySQL database. Here are your options:

#### Option 1: IBM Cloud Databases for MySQL (Recommended for Production)
- Fully managed MySQL service
- Automatic backups and high availability
- Integrated with IBM Cloud
- Cost: ~$100-300/month depending on configuration
- Setup time: 10-15 minutes

#### Option 2: Other Cloud Database Services
- **AWS RDS MySQL**: Managed MySQL on AWS
- **Google Cloud SQL**: Managed MySQL on Google Cloud
- **Azure Database for MySQL**: Managed MySQL on Azure
- **DigitalOcean Managed Databases**: Cost-effective option
- **PlanetScale**: Serverless MySQL with generous free tier

#### Option 3: Self-Hosted MySQL (Development/Testing)
- MySQL on a VM (IBM Cloud Virtual Server, AWS EC2, etc.)
- Docker container on a persistent server
- Not recommended for production
- Requires manual management and backups

#### Option 4: Free Tier Options (Development Only)
- **PlanetScale**: Free tier with 5GB storage
- **Railway**: Free tier with 500MB storage
- **Clever Cloud**: Free tier with 256MB storage
- **Aiven**: Free trial for 30 days

#### Option 5: In-Memory SQLite (Demo/Testing - No External Database Required)
- **SQLite in-memory database** with dummy data
- No external database needed
- Perfect for demos and quick testing
- Data is lost when application restarts
- **Cost**: $0
- **Setup time**: 0 minutes (already configured in code)

**Recommendation**:
- **For Quick Demo**: Use in-memory SQLite (no setup required)
- **For Development**: Use PlanetScale free tier
- **For Production**: Use IBM Cloud Databases for MySQL

### Initial Setup

1. **Login to IBM Cloud**
```bash
ibmcloud login --sso
ibmcloud target -r us-south -g default
```

2. **Create Code Engine project**
```bash
ibmcloud ce project create --name fleet-management
ibmcloud ce project select --name fleet-management
```

3. **Create Container Registry namespace** (if not exists)
```bash
ibmcloud cr namespace-add fleet-management
```

### Deploy with In-Memory SQLite (No External Database Required)

**Perfect for demos and quick testing!** The application can run with an in-memory SQLite database and auto-generated dummy data.

1. **Build and push Docker image**
```bash
# Login to IBM Container Registry
ibmcloud cr login

# Build and push backend with SQLite support
docker build -t us.icr.io/fleet-management/backend:latest ./backend
docker push us.icr.io/fleet-management/backend:latest
```

2. **Create secrets for SQLite mode**
```bash
ibmcloud ce secret create --name app-config \
  --from-literal DATABASE_URL="sqlite:///./fleet_management.db" \
  --from-literal USE_SQLITE="true" \
  --from-literal GENERATE_DUMMY_DATA="true" \
  --from-literal SECRET_KEY="demo-secret-key-change-in-production"
```

3. **Deploy backend application**
```bash
ibmcloud ce application create --name fleet-backend \
  --image us.icr.io/fleet-management/backend:latest \
  --registry-secret icr-secret \
  --env-from-secret app-config \
  --port 8000 \
  --min-scale 1 \
  --max-scale 5 \
  --cpu 0.5 \
  --memory 1G \
  --concurrency 100
```

**Note**: Data will be regenerated each time the application restarts. For persistent data, use one of the MySQL options below.

### Deploy MySQL Database (For Persistent Data)

1. **Create MySQL service instance**
```bash
ibmcloud resource service-instance-create fleet-mysql \
  databases-for-mysql standard us-south \
  -p '{"members_memory_allocation_mb": "3072", "members_disk_allocation_mb": "20480"}'
```

2. **Create service credentials**
```bash
ibmcloud resource service-key-create fleet-mysql-key \
  --instance-name fleet-mysql
```

3. **Get connection string**
```bash
ibmcloud resource service-key fleet-mysql-key
```

### Deploy Backend Application

1. **Build and push Docker image**
```bash
# Login to IBM Container Registry
ibmcloud cr login

# Build and push backend
docker build -t us.icr.io/fleet-management/backend:latest ./backend
docker push us.icr.io/fleet-management/backend:latest
```

2. **Create secrets for database connection**
```bash
ibmcloud ce secret create --name mysql-credentials \
  --from-literal DATABASE_URL="mysql+pymysql://user:pass@host:port/fleet_management" \
  --from-literal SECRET_KEY="your-secret-key"
```

3. **Deploy backend application**
```bash
ibmcloud ce application create --name fleet-backend \
  --image us.icr.io/fleet-management/backend:latest \
  --registry-secret icr-secret \
  --env-from-secret mysql-credentials \
  --port 8000 \
  --min-scale 1 \
  --max-scale 10 \
  --cpu 0.5 \
  --memory 1G \
  --concurrency 100
```

### Deploy Frontend Application

1. **Build and push frontend image**
```bash
docker build -t us.icr.io/fleet-management/frontend:latest ./frontend
docker push us.icr.io/fleet-management/frontend:latest
```

2. **Create configmap for frontend**
```bash
ibmcloud ce configmap create --name frontend-config \
  --from-literal VITE_API_URL="https://fleet-backend.xxx.us-south.codeengine.appdomain.cloud"
```

3. **Deploy frontend application**
```bash
ibmcloud ce application create --name fleet-frontend \
  --image us.icr.io/fleet-management/frontend:latest \
  --registry-secret icr-secret \
  --env-from-configmap frontend-config \
  --port 80 \
  --min-scale 1 \
  --max-scale 5 \
  --cpu 0.25 \
  --memory 512M
```

### Manage Applications

**View applications**
```bash
ibmcloud ce application list
ibmcloud ce application get --name fleet-backend
```

**View logs**
```bash
ibmcloud ce application logs --name fleet-backend
ibmcloud ce application logs --name fleet-backend --follow
```

**Update application**
```bash
ibmcloud ce application update --name fleet-backend \
  --image us.icr.io/fleet-management/backend:v2.0
```

**Scale application**
```bash
ibmcloud ce application update --name fleet-backend \
  --min-scale 2 --max-scale 20
```

**Delete application**
```bash
ibmcloud ce application delete --name fleet-backend
```

### Code Engine Benefits

- ✅ **Serverless**: No cluster management required
- ✅ **Auto-scaling**: Scales to zero when idle, scales up on demand
- ✅ **Cost-effective**: Pay only for actual usage (CPU/memory seconds)
- ✅ **Fast deployment**: Deploy in seconds, not minutes
- ✅ **Built-in CI/CD**: Integrates with GitHub for automated builds
- ✅ **Managed infrastructure**: IBM handles updates and maintenance
- ✅ **HTTPS by default**: Automatic SSL certificates
- ✅ **Custom domains**: Support for custom domain mapping

## 🏗️ Infrastructure as Code (Terraform)

### Initialize Terraform
```bash
cd infrastructure
terraform init
```

### Plan infrastructure changes
```bash
terraform plan -var-file=environments/dev/terraform.tfvars
```

### Apply infrastructure
```bash
terraform apply -var-file=environments/dev/terraform.tfvars
```

### Destroy infrastructure
```bash
terraform destroy -var-file=environments/dev/terraform.tfvars
```

## 🔄 CI/CD Pipeline

The project includes comprehensive GitHub Actions workflows for automated testing, building, and deployment to IBM Code Engine.

### Workflow Overview

```
┌─────────────────┐
│  Push to main   │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌──────────┐
│Backend │ │ Frontend │
│  CI    │ │    CI    │
└───┬────┘ └────┬─────┘
    │           │
    └─────┬─────┘
          ▼
    ┌──────────┐
    │  Build & │
    │   Push   │
    └─────┬────┘
          ▼
    ┌──────────┐
    │  Deploy  │
    │   to CE  │
    └──────────┘
```

### 1. Backend CI Workflow (`.github/workflows/backend-ci.yml`)

Triggers on push/PR to backend files:
- Linting with flake8 and black
- Type checking with mypy
- Unit tests with pytest
- Code coverage reporting
- Security scanning with bandit
- Build Docker image
- Push to IBM Container Registry

### 2. Frontend CI Workflow (`.github/workflows/frontend-ci.yml`)

Triggers on push/PR to frontend files:
- ESLint and Prettier checks
- TypeScript compilation
- Unit tests with Vitest
- Build production bundle
- Build Docker image
- Push to IBM Container Registry

### 3. Code Engine Deployment Workflow (`.github/workflows/deploy-code-engine.yml`)

Triggers on push to main branch (after CI passes):
- Authenticates with IBM Cloud
- Selects Code Engine project
- Updates backend application with new image
- Updates frontend application with new image
- Runs smoke tests
- Sends deployment notifications

### 4. Terraform Workflow (`.github/workflows/terraform.yml`)

Triggers on changes to infrastructure files:
- Validates Terraform configuration
- Runs `terraform plan`
- Applies changes on approval (main branch only)
- Manages IBM Cloud resources

### Sample GitHub Actions Workflow

**`.github/workflows/deploy-code-engine.yml`**
```yaml
name: Deploy to IBM Code Engine

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  IBM_CLOUD_REGION: us-south
  CODE_ENGINE_PROJECT: fleet-management
  REGISTRY_NAMESPACE: fleet-management

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install IBM Cloud CLI
        run: |
          curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
          ibmcloud plugin install code-engine
          ibmcloud plugin install container-registry
      
      - name: Authenticate with IBM Cloud
        run: |
          ibmcloud login --apikey ${{ secrets.IBM_CLOUD_API_KEY }} -r ${{ env.IBM_CLOUD_REGION }}
          ibmcloud cr login
      
      - name: Build and Push Backend Image
        run: |
          docker build -t us.icr.io/${{ env.REGISTRY_NAMESPACE }}/backend:${{ github.sha }} ./backend
          docker tag us.icr.io/${{ env.REGISTRY_NAMESPACE }}/backend:${{ github.sha }} \
                     us.icr.io/${{ env.REGISTRY_NAMESPACE }}/backend:latest
          docker push us.icr.io/${{ env.REGISTRY_NAMESPACE }}/backend:${{ github.sha }}
          docker push us.icr.io/${{ env.REGISTRY_NAMESPACE }}/backend:latest
      
      - name: Deploy to Code Engine
        run: |
          ibmcloud ce project select --name ${{ env.CODE_ENGINE_PROJECT }}
          ibmcloud ce application update --name fleet-backend \
            --image us.icr.io/${{ env.REGISTRY_NAMESPACE }}/backend:${{ github.sha }}
      
      - name: Verify Deployment
        run: |
          ibmcloud ce application get --name fleet-backend
          URL=$(ibmcloud ce application get --name fleet-backend --output json | jq -r '.status.url')
          curl -f $URL/health || exit 1

  deploy-frontend:
    runs-on: ubuntu-latest
    needs: deploy-backend
    steps:
      - uses: actions/checkout@v4
      
      - name: Install IBM Cloud CLI
        run: |
          curl -fsSL https://clis.cloud.ibm.com/install/linux | sh
          ibmcloud plugin install code-engine
          ibmcloud plugin install container-registry
      
      - name: Authenticate with IBM Cloud
        run: |
          ibmcloud login --apikey ${{ secrets.IBM_CLOUD_API_KEY }} -r ${{ env.IBM_CLOUD_REGION }}
          ibmcloud cr login
      
      - name: Build and Push Frontend Image
        run: |
          docker build -t us.icr.io/${{ env.REGISTRY_NAMESPACE }}/frontend:${{ github.sha }} ./frontend
          docker tag us.icr.io/${{ env.REGISTRY_NAMESPACE }}/frontend:${{ github.sha }} \
                     us.icr.io/${{ env.REGISTRY_NAMESPACE }}/frontend:latest
          docker push us.icr.io/${{ env.REGISTRY_NAMESPACE }}/frontend:${{ github.sha }}
          docker push us.icr.io/${{ env.REGISTRY_NAMESPACE }}/frontend:latest
      
      - name: Deploy to Code Engine
        run: |
          ibmcloud ce project select --name ${{ env.CODE_ENGINE_PROJECT }}
          ibmcloud ce application update --name fleet-frontend \
            --image us.icr.io/${{ env.REGISTRY_NAMESPACE }}/frontend:${{ github.sha }}
      
      - name: Verify Deployment
        run: |
          ibmcloud ce application get --name fleet-frontend
          URL=$(ibmcloud ce application get --name fleet-frontend --output json | jq -r '.status.url')
          curl -f $URL || exit 1
```

### Required GitHub Secrets

Configure these secrets in your GitHub repository settings:

**IBM Cloud Authentication**
- `IBM_CLOUD_API_KEY` - IBM Cloud API key with Code Engine and Container Registry permissions
- `IBM_CLOUD_REGION` - IBM Cloud region (e.g., `us-south`, `eu-de`)

**Container Registry**
- `IBM_CR_NAMESPACE` - Container Registry namespace name

**Database Configuration (Skip if using SQLite)**
- `DATABASE_URL` - MySQL connection string (or `sqlite:///./fleet_management.db` for SQLite)
- `MYSQL_ROOT_PASSWORD` - MySQL root password (not needed for SQLite)
- `MYSQL_PASSWORD` - Application MySQL user password (not needed for SQLite)

**Application Secrets**
- `SECRET_KEY` - Application secret key for JWT/sessions
- `CORS_ORIGINS` - Allowed CORS origins (comma-separated)

**SQLite Mode (Optional - For Demo Without External Database)**
- `USE_SQLITE` - Set to `"true"` to use in-memory SQLite instead of MySQL
- `GENERATE_DUMMY_DATA` - Set to `"true"` to auto-generate dummy data on startup

**Code Engine Configuration**
- `CODE_ENGINE_PROJECT` - Code Engine project name
- `BACKEND_APP_NAME` - Backend application name (default: `fleet-backend`)
- `FRONTEND_APP_NAME` - Frontend application name (default: `fleet-frontend`)

### Setting Up GitHub Secrets

**For SQLite Mode (No External Database):**
```bash
# Using GitHub CLI - Minimal setup for demo
gh secret set IBM_CLOUD_API_KEY
gh secret set IBM_CLOUD_REGION -b "us-south"
gh secret set IBM_CR_NAMESPACE -b "fleet-management"
gh secret set DATABASE_URL -b "sqlite:///./fleet_management.db"
gh secret set USE_SQLITE -b "true"
gh secret set GENERATE_DUMMY_DATA -b "true"
gh secret set SECRET_KEY -b "demo-secret-key-change-in-production"
gh secret set CODE_ENGINE_PROJECT -b "fleet-management"
```

**For MySQL Mode (With External Database):**
```bash
# Using GitHub CLI - Full setup with MySQL
gh secret set IBM_CLOUD_API_KEY
gh secret set IBM_CLOUD_REGION -b "us-south"
gh secret set IBM_CR_NAMESPACE -b "fleet-management"
gh secret set DATABASE_URL  # Enter your MySQL connection string
gh secret set SECRET_KEY
gh secret set CODE_ENGINE_PROJECT -b "fleet-management"
```

### Deployment Strategies

**1. Continuous Deployment (CD)**
- Automatic deployment on every push to `main`
- Suitable for development environments
- Fast feedback loop

**2. Manual Approval**
- Deployment requires manual approval
- Suitable for staging/production
- Add `environment` protection rules in GitHub

**3. Blue-Green Deployment**
- Deploy to new version alongside old
- Switch traffic after verification
- Zero-downtime deployments

**4. Canary Deployment**
- Gradually shift traffic to new version
- Monitor metrics and rollback if needed
- Minimize risk of bad deployments

### Monitoring Deployments

**View deployment status**
```bash
ibmcloud ce application list
ibmcloud ce application events --application fleet-backend
```

**Check application logs**
```bash
ibmcloud ce application logs --name fleet-backend --follow
```

**View revision history**
```bash
ibmcloud ce revision list --application fleet-backend
```

**Rollback to previous version**
```bash
ibmcloud ce application update --name fleet-backend \
  --image us.icr.io/fleet-management/backend:previous-sha
```

## 📈 Monitoring

### Health Checks
- Application health: `GET /health`
- Readiness: `GET /ready`
- Liveness: `GET /live`

### Metrics
- Prometheus metrics: `GET /metrics`
- Event queue stats: `GET /api/v1/status`

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 📝 Development Workflow

1. Create feature branch
2. Make changes
3. Run tests locally
4. Commit and push
5. Create pull request
6. CI/CD pipeline runs automatically
7. Review and merge
8. Automatic deployment to dev environment

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- DevOps Team

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the frontend library
- IBM Cloud for hosting infrastructure
- Open source community

## 📞 Support

For support, email support@fleetmanagement.com or open an issue in the repository.

---

**Built with ❤️ for DevOps demonstration**