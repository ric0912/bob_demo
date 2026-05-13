#!/bin/bash

# Setup script for SQLite demo mode (no external database required)

echo "=========================================="
echo "Fleet Management - SQLite Demo Setup"
echo "=========================================="
echo ""

# Create .env file for backend
echo "Creating backend .env file for SQLite mode..."
cat > backend/.env << EOF
# Database Configuration - SQLite Mode
DATABASE_URL=sqlite:///./fleet_management.db
USE_SQLITE=true
GENERATE_DUMMY_DATA=true

# Application Settings
APP_NAME=Fleet Management Platform
APP_VERSION=1.0.0
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# Security
SECRET_KEY=demo-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://localhost:8080

# Event Queue
EVENT_QUEUE_MAX_SIZE=1000
EVENT_PROCESSING_INTERVAL=0.1

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
EOF

echo "✓ Backend .env file created"

# Create .env file for frontend
echo "Creating frontend .env file..."
cat > frontend/.env << EOF
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_ENVIRONMENT=development
EOF

echo "✓ Frontend .env file created"

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Your application is configured to use SQLite with dummy data."
echo ""
echo "To start the application:"
echo "  1. Using Docker Compose:"
echo "     docker-compose up -d"
echo ""
echo "  2. Manual start:"
echo "     Backend:  cd backend && uvicorn app.main:app --reload"
echo "     Frontend: cd frontend && npm run dev"
echo ""
echo "The application will automatically:"
echo "  ✓ Create an in-memory SQLite database"
echo "  ✓ Generate 10 dummy vehicles"
echo "  ✓ Generate telemetry data"
echo "  ✓ Create fleet assignments"
echo "  ✓ Generate sample alerts"
echo ""
echo "Access the application at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Note: Data will be regenerated each time the backend restarts."
echo "=========================================="

# Made with Bob
