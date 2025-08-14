

"""
AI-DE Pair Backend - SQL Generation System
==========================================

Clean, documented implementation following our comprehensive requirements.
Retains /run-sql endpoint for frontend testing while building the new AI system.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# from databricks import sql  # Commented out for testing
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
import sys
import os

# Import from our app structure
from app.db.database import get_db, init_db
from app.services.database_service import SessionService, AIMemoryCacheService
from app.schemas import (
    CreateSessionRequest, SessionResponse, APIStatusResponse, 
    HealthCheckResponse, ErrorResponse
)
from app.db.models import SessionStatus
from datetime import datetime
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-DE Pair Backend",
    description="AI-powered SQL generation from Excel mapping documents",
    version="0.1.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================
# STARTUP AND SHUTDOWN EVENTS
# ================================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting AI-DE Pair Backend...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down AI-DE Pair Backend...")


# ================================
# REQUEST/RESPONSE MODELS
# ================================

class SQLRequest(BaseModel):
    """Request model for direct SQL execution (frontend testing)"""
    sql: str
    server_hostname: str
    http_path: str
    access_token: str


# ================================
# CORE ENDPOINTS
# ================================

@app.get("/")
def read_root():
    """Health check and welcome endpoint"""
    return {
        "message": "AI-DE Pair Backend - SQL Generation System",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthCheckResponse)
def health_check(db: Session = Depends(get_db)):
    """Detailed health check endpoint with database status"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        database_status = "connected"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        database_status = "disconnected"
    
    return HealthCheckResponse(
        status="healthy" if database_status == "connected" else "degraded",
        service="ai-de-pair-backend",
        version="0.1.0",
        timestamp=datetime.now(),
        database_status=database_status
    )



# ================================
# SESSION MANAGEMENT ENDPOINTS
# ================================

@app.post("/ai/sessions", response_model=SessionResponse)
def create_session(request: CreateSessionRequest, db: Session = Depends(get_db)):
    """
    Create a new analysis session
    
    IMPLEMENTED: Phase 1 - Session management with database tracking
    """
    try:
        session = SessionService.create_session(db, request)
        logger.info(f"Created new session: {session.id}")
        return session
    except Exception as e:
        logger.error(f"Failed to create session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@app.get("/ai/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: str, db: Session = Depends(get_db)):
    """
    Get session information by ID
    
    IMPLEMENTED: Phase 1 - Session retrieval
    """
    session = SessionService.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/ai/sessions", response_model=List[SessionResponse])
def list_recent_sessions(limit: int = 10, db: Session = Depends(get_db)):
    """
    List recent analysis sessions
    
    IMPLEMENTED: Phase 1 - Session listing
    """
    sessions = SessionService.get_recent_sessions(db, limit)
    return sessions


# ================================
# FRONTEND TESTING ENDPOINTS
# ================================

@app.post("/run-sql")
def run_sql(request: SQLRequest):
    """
    Direct SQL execution endpoint for frontend testing
    
    RETAINED: This endpoint is kept for frontend testing purposes.
    Executes SQL directly against Databricks without AI processing.
    """
    logger.info(f"Executing SQL query: {request.sql[:100]}...")
    
    try:
        with sql.connect(
            server_hostname=request.server_hostname,
            http_path=request.http_path,
            access_token=request.access_token
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(request.sql)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                results = [dict(zip(columns, row)) for row in rows]
        
        logger.info(f"SQL execution successful. Returned {len(results)} rows.")
        return {"results": results}
        
    except Exception as e:
        logger.error(f"SQL execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ================================
# AI SQL GENERATION ENDPOINTS (TO BE IMPLEMENTED)
# ================================

@app.post("/ai/excel/upload")
async def upload_excel_mapping():
    """
    TODO: Phase 2 - Excel file upload and initial processing
    
    Will handle:
    - Excel file upload
    - Sheet extraction and parsing
    - Content analysis and pattern detection
    """
    return {"status": "not_implemented", "phase": "2", "message": "Excel upload endpoint - coming soon"}


@app.post("/ai/discover/information")
async def discover_information():
    """
    TODO: Phase 3 - Information discovery system
    
    Will handle:
    - Sheet pattern scanning
    - Information location mapping
    - Discovery question generation
    """
    return {"status": "not_implemented", "phase": "3", "message": "Information discovery - coming soon"}


@app.post("/ai/strategic/clarification")
async def strategic_clarification():
    """
    TODO: Phase 5 - Strategic clarification system
    
    Will handle:
    - Multi-table detection questions
    - Transformation strategy questions
    - Join strategy analysis
    - Chat-based clarification
    """
    return {"status": "not_implemented", "phase": "5", "message": "Strategic clarification - coming soon"}


@app.post("/ai/generate/sql")
async def generate_sql():
    """
    TODO: Phase 6 - SQL generation engine
    
    Will handle:
    - Single query generation
    - Multiple query generation
    - Sequential pipeline generation
    - SQL validation and optimization
    """
    return {"status": "not_implemented", "phase": "6", "message": "AI SQL generation - coming soon"}


@app.get("/ai/generate/sql/sse")
async def generate_sql_sse():
    """
    TODO: Phase 7 - Real-time SQL generation with SSE
    
    Will handle:
    - Real-time progress updates
    - Event broadcasting
    - Client connection management
    """
    return {"status": "not_implemented", "phase": "7", "message": "SSE SQL generation - coming soon"}


# ================================
# SYSTEM STATUS ENDPOINTS
# ================================

@app.get("/api/status", response_model=APIStatusResponse)
def api_status(db: Session = Depends(get_db)):
    """API implementation status overview with database statistics"""
    try:
        # Get database statistics
        total_sessions = len(SessionService.get_recent_sessions(db, limit=1000))
        cache_stats = AIMemoryCacheService.get_cache_statistics(db)
        database_initialized = True
    except Exception as e:
        logger.error(f"Database query failed in status check: {str(e)}")
        total_sessions = 0
        database_initialized = False
    
    return APIStatusResponse(
        implementation_status={
            "phase_1_foundation": "✅ IMPLEMENTED - Database models, session management",
            "phase_2_excel_processing": "📋 Planned",
            "phase_3_information_discovery": "📋 Planned", 
            "phase_4_ai_analysis": "📋 Planned",
            "phase_5_strategic_clarification": "📋 Planned",
            "phase_6_sql_generation": "📋 Planned",
            "phase_7_sse_implementation": "📋 Planned",
            "phase_8_performance": "📋 Planned",
            "phase_9_testing": "📋 Planned",
            "phase_10_documentation": "📋 Planned"
        },
        current_endpoints={
            "working": ["/", "/health", "/run-sql", "/ai/sessions"],
            "planned": [
                "/ai/excel/upload",
                "/ai/discover/information", 
                "/ai/strategic/clarification",
                "/ai/generate/sql",
                "/ai/generate/sql/sse"
            ]
        },
        next_implementation="Phase 2: Excel processing engine",
        database_initialized=database_initialized,
        total_sessions=total_sessions
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
