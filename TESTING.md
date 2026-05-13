# Fleet Management Platform - Testing Documentation

## Overview

This document provides comprehensive testing guidelines for the Fleet Management Platform. The project includes unit tests, integration tests, and end-to-end tests for both backend (FastAPI) and frontend (React) components.

## Table of Contents

1. [Backend Testing](#backend-testing)
2. [Frontend Testing](#frontend-testing)
3. [Running Tests](#running-tests)
4. [Test Coverage](#test-coverage)
5. [Writing New Tests](#writing-new-tests)
6. [CI/CD Integration](#cicd-integration)

---

## Backend Testing

### Technology Stack

- **Framework**: pytest
- **Async Support**: pytest-asyncio
- **HTTP Testing**: FastAPI TestClient
- **Database**: SQLite (in-memory for tests)
- **Coverage**: pytest-cov

### Test Structure

```
backend/
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini               # Pytest settings
└── tests/
    ├── __init__.py
    ├── test_api_vehicles.py      # Vehicle API tests
    ├── test_api_telemetry.py     # Telemetry API tests
    ├── test_api_fleet.py         # Fleet management tests
    ├── test_api_analytics.py     # Analytics API tests
    └── test_integration_workflows.py  # Integration tests
```

### Test Categories

#### 1. Unit Tests (`@pytest.mark.unit`)
- Test individual API endpoints
- Test database models
- Test business logic functions
- Fast execution, isolated tests

#### 2. Integration Tests (`@pytest.mark.integration`)
- Test complete workflows
- Test multiple components together
- Test real-world scenarios

#### 3. Database Tests (`@pytest.mark.database`)
- Test database operations
- Test model constraints
- Test data integrity

### Key Test Files

#### `test_api_vehicles.py`
Tests for vehicle management:
- Vehicle CRUD operations
- Vehicle status management
- Pagination
- Error handling
- Event publishing

#### `test_api_telemetry.py`
Tests for telemetry data:
- Telemetry submission
- Vehicle-specific telemetry retrieval
- Latest telemetry queries
- Data validation

#### `test_api_fleet.py`
Tests for fleet operations:
- Fleet overview statistics
- Assignment creation and management
- Alert management
- Status transitions

#### `test_api_analytics.py`
Tests for analytics:
- Summary statistics
- Vehicle-specific analytics
- Performance metrics
- Trend analysis

#### `test_integration_workflows.py`
End-to-end workflow tests:
- Complete vehicle lifecycle
- Multi-vehicle fleet operations
- Telemetry streaming
- Alert management workflow
- Error handling scenarios

### Running Backend Tests

```bash
# Navigate to backend directory
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api_vehicles.py

# Run specific test class
pytest tests/test_api_vehicles.py::TestVehicleAPI

# Run specific test
pytest tests/test_api_vehicles.py::TestVehicleAPI::test_create_vehicle_success

# Run tests by marker
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m "not slow"    # Skip slow tests

# Run with verbose output
pytest -v

# Run with detailed output
pytest -vv

# Stop on first failure
pytest -x
```

### Backend Test Fixtures

Available fixtures in `conftest.py`:

- `db`: Fresh database session for each test
- `client`: FastAPI test client with database override
- `sample_vehicle_data`: Mock vehicle data
- `sample_telemetry_data`: Mock telemetry data
- `sample_fleet_assignment_data`: Mock assignment data
- `multiple_vehicles_data`: Multiple vehicles for list tests

---

## Frontend Testing

### Technology Stack

- **Framework**: Vitest
- **Testing Library**: React Testing Library
- **Mocking**: Vitest mocks
- **Coverage**: Vitest coverage (v8)

### Test Structure

```
frontend/
├── vitest.config.ts         # Vitest configuration
└── src/
    └── tests/
        ├── setup.ts                    # Test setup and global mocks
        ├── components/
        │   └── VehicleList.test.tsx   # Component tests
        └── services/
            └── api.test.ts            # API service tests
```

### Test Categories

#### 1. Component Tests
- Test React component rendering
- Test user interactions
- Test component state management
- Test props and callbacks

#### 2. Service Tests
- Test API calls
- Test error handling
- Test data transformation
- Test request/response handling

### Key Test Files

#### `VehicleList.test.tsx`
Tests for VehicleList component:
- Loading states
- Data rendering
- Empty states
- Error handling
- Status display

#### `api.test.ts`
Tests for API service:
- Vehicle API endpoints
- Telemetry API endpoints
- Fleet API endpoints
- Analytics API endpoints
- Error handling (404, 400, 500, network errors)

### Running Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage

# Run specific test file
npm test VehicleList.test.tsx

# Run tests with UI
npm run test:ui
```

### Frontend Test Utilities

Available in `setup.ts`:

- Jest-DOM matchers extended to Vitest
- Automatic cleanup after each test
- Mock for `window.matchMedia`
- Mock for `IntersectionObserver`
- Mock for `ResizeObserver`

---

## Test Coverage

### Backend Coverage Goals

- **Overall**: > 80%
- **API Endpoints**: > 90%
- **Models**: > 85%
- **Services**: > 80%

### Frontend Coverage Goals

- **Overall**: > 75%
- **Components**: > 80%
- **Services**: > 85%
- **Utilities**: > 80%

### Viewing Coverage Reports

#### Backend
```bash
cd backend
pytest --cov=app --cov-report=html
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
```

#### Frontend
```bash
cd frontend
npm run test:coverage
open coverage/index.html  # macOS
# or
xdg-open coverage/index.html  # Linux
```

---

## Writing New Tests

### Backend Test Template

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

@pytest.mark.unit
class TestNewFeature:
    """Test suite for new feature"""
    
    def test_feature_success(self, client: TestClient, db: Session):
        """Test successful feature operation"""
        # Arrange
        test_data = {"key": "value"}
        
        # Act
        response = client.post("/api/v1/endpoint", json=test_data)
        
        # Assert
        assert response.status_code == 201
        assert response.json()["key"] == "value"
    
    def test_feature_error(self, client: TestClient):
        """Test feature error handling"""
        # Arrange
        invalid_data = {}
        
        # Act
        response = client.post("/api/v1/endpoint", json=invalid_data)
        
        # Assert
        assert response.status_code == 422
```

### Frontend Test Template

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { NewComponent } from './NewComponent';

describe('NewComponent', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render successfully', () => {
    render(<NewComponent />);
    
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });

  it('should handle user interaction', async () => {
    render(<NewComponent />);
    
    const button = screen.getByRole('button');
    button.click();
    
    await waitFor(() => {
      expect(screen.getByText('Result')).toBeInTheDocument();
    });
  });
});
```

---

## Best Practices

### General

1. **Follow AAA Pattern**: Arrange, Act, Assert
2. **One Assertion Per Test**: Focus on single behavior
3. **Descriptive Names**: Test names should describe what they test
4. **Independent Tests**: Tests should not depend on each other
5. **Clean Up**: Always clean up resources after tests

### Backend

1. **Use Fixtures**: Leverage pytest fixtures for common setup
2. **Mock External Services**: Don't make real API calls
3. **Test Edge Cases**: Include boundary conditions
4. **Test Error Paths**: Verify error handling
5. **Use Markers**: Tag tests appropriately (unit, integration, slow)

### Frontend

1. **Test User Behavior**: Focus on what users see and do
2. **Avoid Implementation Details**: Don't test internal state
3. **Use Testing Library Queries**: Prefer accessible queries
4. **Mock API Calls**: Use vi.mock for external dependencies
5. **Test Loading States**: Include loading and error states

---

## CI/CD Integration

### GitHub Actions

Tests run automatically on:
- Pull requests
- Pushes to main branch
- Manual workflow dispatch

### Required Checks

- All backend tests must pass
- All frontend tests must pass
- Coverage thresholds must be met
- No linting errors

### Local Pre-commit

Run before committing:

```bash
# Backend
cd backend && pytest

# Frontend
cd frontend && npm test

# Both
./scripts/run-all-tests.sh  # If available
```

---

## Troubleshooting

### Common Issues

#### Backend

**Issue**: Database connection errors
```bash
# Solution: Ensure test database is properly configured
# Check conftest.py for database setup
```

**Issue**: Import errors
```bash
# Solution: Ensure PYTHONPATH is set correctly
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### Frontend

**Issue**: Module not found errors
```bash
# Solution: Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Issue**: Test timeouts
```bash
# Solution: Increase timeout in vitest.config.ts
test: {
  testTimeout: 10000
}
```

---

## Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Testing Best Practices](https://testingjavascript.com/)

---

## Contributing

When adding new features:

1. Write tests first (TDD approach recommended)
2. Ensure all tests pass
3. Maintain or improve coverage
4. Update this documentation if needed
5. Add test examples for complex scenarios

---

## Contact

For questions about testing:
- Review existing tests for examples
- Check this documentation
- Consult with the development team

---

**Last Updated**: 2026-05-13
**Version**: 1.0.0