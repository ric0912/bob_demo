"""
Main FastAPI application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time

from app.config import settings
from app.database import init_db, SessionLocal
from app.events import event_queue, register_event_handlers
from app.api import vehicles, telemetry, fleet, analytics, websocket
from app.services.telemetry_simulator import telemetry_simulator
from app.seed_data import generate_dummy_data

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("Starting Fleet Management Platform...")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
        
        # Generate dummy data if enabled
        if settings.GENERATE_DUMMY_DATA:
            logger.info("Dummy data generation enabled")
            db = SessionLocal()
            try:
                generate_dummy_data(db)
            except Exception as e:
                logger.error(f"Dummy data generation failed: {e}")
            finally:
                db.close()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    # Start event queue
    try:
        register_event_handlers(event_queue)
        await event_queue.start()
        logger.info("Event queue started successfully")
    except Exception as e:
        logger.error(f"Event queue startup failed: {e}")
        raise
    
    # Start WebSocket event listener
    try:
        await websocket.manager.listen_to_events()
        logger.info("WebSocket event listener started")
    except Exception as e:
        logger.error(f"WebSocket listener startup failed: {e}")
    
    # Start telemetry simulator
    try:
        await telemetry_simulator.start()
        logger.info("Telemetry simulator started (generating real-time data)")
    except Exception as e:
        logger.error(f"Telemetry simulator startup failed: {e}")
    
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Fleet Management Platform...")
    
    # Stop telemetry simulator
    try:
        await telemetry_simulator.stop()
        logger.info("Telemetry simulator stopped")
    except Exception as e:
        logger.error(f"Telemetry simulator shutdown failed: {e}")
    
    # Stop event queue
    try:
        await event_queue.stop()
        logger.info("Event queue stopped successfully")
    except Exception as e:
        logger.error(f"Event queue shutdown failed: {e}")
    
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Fleet Management Platform for Autonomous Vehicles",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Returns the health status of the application
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


# Readiness check endpoint
@app.get("/ready", tags=["Health"])
async def readiness_check():
    """
    Readiness check endpoint
    Returns whether the application is ready to serve requests
    """
    event_stats = event_queue.get_stats()
    
    return {
        "status": "ready",
        "database": "connected",
        "event_queue": {
            "running": event_stats["running"],
            "queue_size": event_stats["queue_size"]
        }
    }


# Liveness check endpoint
@app.get("/live", tags=["Health"])
async def liveness_check():
    """
    Liveness check endpoint
    Returns whether the application is alive
    """
    return {"status": "alive"}


# System status endpoint
@app.get("/api/v1/status", tags=["System"])
async def system_status():
    """
    Get system status and statistics
    """
    event_stats = event_queue.get_stats()
    
    return {
        "application": {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT
        },
        "event_queue": event_stats
    }


# Metrics endpoint for Prometheus
@app.get("/metrics", tags=["Monitoring"])
async def metrics():
    """
    Prometheus metrics endpoint
    """
    # This is a placeholder - in production, use prometheus_client
    return {
        "metrics": "prometheus_metrics_here"
    }


# Include API routers
app.include_router(
    vehicles.router,
    prefix=settings.API_V1_PREFIX,
    tags=["Vehicles"]
)

app.include_router(
    telemetry.router,
    prefix=settings.API_V1_PREFIX,
    tags=["Telemetry"]
)

app.include_router(
    fleet.router,
    prefix=settings.API_V1_PREFIX,
    tags=["Fleet"]
)

app.include_router(
    analytics.router,
    prefix=settings.API_V1_PREFIX,
    tags=["Analytics"]
)

app.include_router(
    websocket.router,
    tags=["WebSocket"]
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Fleet Management Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

# Made with Bob
