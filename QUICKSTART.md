# Quick Start Guide - SQLite Demo Mode

This guide will help you get the Fleet Management Platform running in **demo mode** using SQLite with auto-generated dummy data - **no external database required!**

## 🚀 Fastest Way to Start (5 minutes)

### Option 1: Automated Setup Script

```bash
# Run the setup script
./scripts/setup-sqlite-demo.sh

# Start with Docker Compose
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### Backend Setup

1. **Create backend .env file:**
```bash
cd backend
cat > .env << EOF
DATABASE_URL=sqlite:///./fleet_management.db
USE_SQLITE=true
GENERATE_DUMMY_DATA=true
SECRET_KEY=demo-secret-key
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
EOF
```

2. **Install dependencies and run:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

1. **Create frontend .env file:**
```bash
cd frontend
cat > .env << EOF
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
EOF
```

2. **Install dependencies and run:**
```bash
npm install
npm run dev
```

## 📊 What You Get

When you start the application in SQLite demo mode, it automatically generates:

- ✅ **10 Autonomous Vehicles** (Tesla, Waymo, Cruise, etc.)
- ✅ **50 Telemetry Records** (GPS, battery, speed data)
- ✅ **5 Fleet Assignments** (active routes)
- ✅ **3 Alerts** (battery low, maintenance, etc.)

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Main dashboard |
| Backend API | http://localhost:8000 | REST API |
| API Documentation | http://localhost:8000/docs | Interactive Swagger UI |
| Health Check | http://localhost:8000/health | Health status |

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```bash
DATABASE_URL=sqlite:///./fleet_management.db  # SQLite database file
USE_SQLITE=true                                # Enable SQLite mode
GENERATE_DUMMY_DATA=true                       # Auto-generate data
SECRET_KEY=demo-secret-key                     # Change in production
CORS_ORIGINS=http://localhost:3000             # Frontend URL
```

**Frontend (.env):**
```bash
VITE_API_URL=http://localhost:8000            # Backend API URL
VITE_WS_URL=ws://localhost:8000               # WebSocket URL
```

## 📝 Important Notes

### SQLite Demo Mode Limitations

- ⚠️ **Data is temporary**: All data is lost when the backend restarts
- ⚠️ **Single instance only**: Cannot scale beyond 1 backend instance
- ⚠️ **Not for production**: Use MySQL/PostgreSQL for production deployments

### When to Use SQLite Mode

✅ **Perfect for:**
- Quick demos and presentations
- Local development and testing
- Learning and experimentation
- CI/CD testing pipelines

❌ **Not suitable for:**
- Production deployments
- Multi-instance deployments
- Persistent data requirements
- High-traffic applications

## 🚀 Deploying to IBM Code Engine (Demo Mode)

You can deploy the SQLite demo mode to IBM Code Engine:

```bash
# Set up Code Engine project
ibmcloud ce project create --name fleet-management
ibmcloud ce project select --name fleet-management

# Create secrets for SQLite mode
ibmcloud ce secret create --name app-config \
  --from-literal DATABASE_URL="sqlite:///./fleet_management.db" \
  --from-literal USE_SQLITE="true" \
  --from-literal GENERATE_DUMMY_DATA="true" \
  --from-literal SECRET_KEY="demo-secret-key"

# Build and push image
docker build -t us.icr.io/fleet-management/backend:latest ./backend
docker push us.icr.io/fleet-management/backend:latest

# Deploy application
ibmcloud ce application create --name fleet-backend \
  --image us.icr.io/fleet-management/backend:latest \
  --env-from-secret app-config \
  --port 8000 \
  --min-scale 1 \
  --max-scale 1 \
  --cpu 0.5 \
  --memory 1G
```

### GitHub Actions Deployment

Set these secrets in your GitHub repository:

```bash
gh secret set IBM_CLOUD_API_KEY
gh secret set DATABASE_URL -b "sqlite:///./fleet_management.db"
gh secret set USE_SQLITE -b "true"
gh secret set GENERATE_DUMMY_DATA -b "true"
gh secret set SECRET_KEY -b "demo-secret-key"
gh secret set CODE_ENGINE_PROJECT -b "fleet-management"
```

Then push to main branch to trigger automatic deployment.

## 🔄 Switching to MySQL

When you're ready to use a persistent database:

1. **Update backend/.env:**
```bash
DATABASE_URL=mysql+pymysql://user:pass@host:3306/fleet_management
USE_SQLITE=false
GENERATE_DUMMY_DATA=false
```

2. **Set up MySQL database:**
```bash
# Using Docker
docker run -d \
  --name mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=fleet_management \
  -e MYSQL_USER=fleetuser \
  -e MYSQL_PASSWORD=fleetpass \
  -p 3306:3306 \
  mysql:8.0

# Initialize database
mysql -h localhost -u fleetuser -pfleetpass fleet_management < scripts/init-db.sql
```

3. **Restart the backend**

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is already in use
lsof -i :8000

# Check backend logs
docker-compose logs backend
```

### Frontend can't connect to backend
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/.env
# Make sure CORS_ORIGINS includes your frontend URL
```

### No data showing up
```bash
# Verify GENERATE_DUMMY_DATA is set to true
cat backend/.env | grep GENERATE_DUMMY_DATA

# Check backend logs for data generation
docker-compose logs backend | grep "dummy data"
```

## 📚 Next Steps

- Read the full [README.md](README.md) for complete documentation
- Check [PLAN.md](PLAN.md) for architecture details
- Explore the API at http://localhost:8000/docs
- Deploy to IBM Code Engine for cloud hosting

## 🤝 Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review the [API documentation](http://localhost:8000/docs)
- Open an issue on GitHub

---

**Happy coding! 🚗💨**