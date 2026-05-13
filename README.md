# Fleet Management Platform

A comprehensive DevOps demonstration project showcasing a full-stack autonomous vehicle fleet management platform with complete CI/CD pipeline, Infrastructure as Code, and cloud deployment on IBM Cloud.

## 🚀 Project Overview

This project demonstrates modern DevOps practices through a real-world autonomous vehicle fleet management application, featuring:

- **Full-Stack Application**: React frontend + FastAPI backend
- **Database**: MySQL 8.0
- **Event-Driven Architecture**: Custom in-memory event queue
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes on IBM Cloud
- **Infrastructure as Code**: Terraform
- **CI/CD**: GitHub Actions
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
- **Orchestration**: Kubernetes
- **IaC**: Terraform
- **CI/CD**: GitHub Actions
- **Cloud**: IBM Cloud

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

The project includes GitHub Actions workflows for:

1. **Backend CI**: Linting, testing, building Docker images
2. **Frontend CI**: Linting, testing, building
3. **Terraform**: Infrastructure validation and deployment
4. **Deployment**: Automated deployment to IBM Cloud

### Required GitHub Secrets
- `IBM_CLOUD_API_KEY`
- `IBM_CLOUD_REGION`
- `IBM_CR_NAMESPACE`
- `MYSQL_ROOT_PASSWORD`
- `MYSQL_PASSWORD`
- `SECRET_KEY`

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