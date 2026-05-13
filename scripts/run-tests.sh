#!/bin/bash

# Fleet Management Platform - Test Runner Script
# This script runs all tests for both backend and frontend

set -e  # Exit on error

echo "=================================="
echo "Fleet Management Platform - Tests"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
    fi
}

# Track overall status
BACKEND_STATUS=0
FRONTEND_STATUS=0

# Backend Tests
echo "Running Backend Tests..."
echo "------------------------"
cd backend

if [ -f "requirements-test.txt" ]; then
    echo "Installing test dependencies..."
    pip install -q -r requirements-test.txt
fi

echo "Running pytest..."
if pytest -v --cov=app --cov-report=term-missing --cov-report=html; then
    BACKEND_STATUS=0
    print_status 0 "Backend tests passed"
else
    BACKEND_STATUS=1
    print_status 1 "Backend tests failed"
fi

cd ..
echo ""

# Frontend Tests
echo "Running Frontend Tests..."
echo "-------------------------"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo "Running vitest..."
if npm test; then
    FRONTEND_STATUS=0
    print_status 0 "Frontend tests passed"
else
    FRONTEND_STATUS=1
    print_status 1 "Frontend tests failed"
fi

cd ..
echo ""

# Summary
echo "=================================="
echo "Test Summary"
echo "=================================="
print_status $BACKEND_STATUS "Backend Tests"
print_status $FRONTEND_STATUS "Frontend Tests"
echo ""

# Exit with error if any tests failed
if [ $BACKEND_STATUS -ne 0 ] || [ $FRONTEND_STATUS -ne 0 ]; then
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
else
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
fi

# Made with Bob
