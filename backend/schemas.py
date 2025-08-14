"""
Pydantic Schemas for API Request/Response Validation
===================================================

Data validation models for the AI SQL generation system.
Defines the structure for API requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum
import uuid


# ================================
# ENUMS FOR API VALIDATION
# ================================

class SessionStatusResponse(str, Enum):
    """Session status for API responses"""
    CREATED = "created"
    PROCESSING_EXCEL = "processing_excel"
    DISCOVERY_QUESTIONS = "discovery_questions"
    AWAITING_USER_INPUT = "awaiting_user_input"
    STRATEGIC_CLARIFICATION = "strategic_clarification"
    GENERATING_SQL = "generating_sql"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class QuestionTypeResponse(str, Enum):
    """Question type for API responses"""
    INFORMATION_DISCOVERY = "information_discovery"
    STRATEGIC_CLARIFICATION = "strategic_clarification"
    TRANSFORMATION_STRATEGY = "transformation_strategy"
    JOIN_STRATEGY = "join_strategy"
    OUTPUT_FORMAT = "output_format"
    MULTI_TABLE_DETECTION = "multi_table_detection"


# ================================
# REQUEST SCHEMAS
# ================================

class CreateSessionRequest(BaseModel):
    """Request to create a new analysis session"""
    filename: Optional[str] = None
    user_id: Optional[str] = None
    ai_provider: str = Field(default="openai", regex="^(openai|claude|local)$")
    connection_details: Optional[Dict[str, Any]] = None


class ExcelUploadRequest(BaseModel):
    """Request for Excel file upload and processing"""
    session_id: str = Field(..., description="Session ID to associate with upload")
    filename: str = Field(..., min_length=1)
    file_content: bytes = Field(..., description="Base64 encoded Excel file content")
    additional_context: Optional[str] = None


class UserResponseRequest(BaseModel):
    """User response to an AI question"""
    session_id: str
    interaction_id: str
    response_data: Union[str, List[str], Dict[str, Any]]
    response_text: Optional[str] = None
    confidence_level: Optional[float] = Field(None, ge=0.0, le=1.0)


class SQLGenerationRequest(BaseModel):
    """Request to generate SQL from analysis"""
    session_id: str
    generation_strategy: str = Field(
        default="single_unified_query",
        regex="^(single_unified_query|multiple_separate_queries|sequential_pipeline)$"
    )
    additional_instructions: Optional[str] = None


# ================================
# RESPONSE SCHEMAS
# ================================

class SessionResponse(BaseModel):
    """Analysis session information"""
    id: str
    status: SessionStatusResponse
    filename: Optional[str]
    current_phase: Optional[str]
    progress_percentage: float
    ai_provider: str
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class ExcelDocumentResponse(BaseModel):
    """Excel document analysis results"""
    id: str
    filename: str
    sheet_count: int
    sheet_names: List[str]
    processing_time_seconds: Optional[float]
    ai_confidence_score: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionOption(BaseModel):
    """Option for multiple choice questions"""
    value: str
    label: str
    description: Optional[str] = None


class AIQuestionResponse(BaseModel):
    """AI question presented to user"""
    id: str
    session_id: str
    question_type: QuestionTypeResponse
    question_text: str
    question_context: Optional[str]
    options: Optional[List[QuestionOption]] = None
    priority: Optional[str]
    sequence_number: Optional[int]
    asked_at: datetime

    class Config:
        from_attributes = True


class AIInteractionResponse(BaseModel):
    """Completed AI interaction with response"""
    id: str
    question_type: QuestionTypeResponse
    question_text: str
    user_response: Optional[Dict[str, Any]]
    response_text: Optional[str]
    confidence_level: Optional[float]
    ai_interpretation: Optional[Dict[str, Any]]
    asked_at: datetime
    answered_at: Optional[datetime]

    class Config:
        from_attributes = True


class SQLGenerationResponse(BaseModel):
    """Generated SQL results"""
    id: str
    generation_strategy: str
    version: int
    sql_content: str
    sql_explanation: Optional[str]
    target_tables: Optional[List[str]]
    validation_status: str
    validation_errors: Optional[List[str]]
    validation_warnings: Optional[List[str]]
    estimated_complexity: Optional[str]
    ai_provider_used: str
    token_usage_input: Optional[int]
    token_usage_output: Optional[int]
    generation_time_seconds: Optional[float]
    cost_estimate: Optional[float]
    generated_at: datetime

    class Config:
        from_attributes = True


class SessionDetailResponse(BaseModel):
    """Complete session information with related data"""
    session: SessionResponse
    excel_documents: List[ExcelDocumentResponse]
    ai_interactions: List[AIInteractionResponse]
    sql_generations: List[SQLGenerationResponse]


# ================================
# SSE EVENT SCHEMAS
# ================================

class SSEEventData(BaseModel):
    """Base structure for SSE events"""
    event_type: str
    session_id: str
    timestamp: datetime
    data: Dict[str, Any]


class ProgressEventData(BaseModel):
    """Progress update event"""
    phase: str
    progress_percentage: float
    message: str
    details: Optional[Dict[str, Any]] = None


class QuestionEventData(BaseModel):
    """New question event"""
    question_id: str
    question_type: str
    question_text: str
    options: Optional[List[QuestionOption]] = None


class SQLGeneratedEventData(BaseModel):
    """SQL generation completed event"""
    generation_id: str
    sql_content: str
    validation_status: str
    performance_analysis: Optional[Dict[str, Any]] = None


class ErrorEventData(BaseModel):
    """Error event"""
    error_type: str
    error_message: str
    error_details: Optional[Dict[str, Any]] = None


# ================================
# UTILITY SCHEMAS
# ================================

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    service: str = "ai-de-pair-backend"
    version: str = "0.1.0"
    timestamp: datetime
    database_status: str
    ai_provider_status: Optional[Dict[str, str]] = None


class APIStatusResponse(BaseModel):
    """API implementation status"""
    implementation_status: Dict[str, str]
    current_endpoints: Dict[str, List[str]]
    next_implementation: str
    database_initialized: bool
    total_sessions: int


# ================================
# VALIDATORS
# ================================

class BaseSchema(BaseModel):
    """Base schema with common validators"""
    
    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        """Convert empty strings to None"""
        if v == '':
            return None
        return v


# ================================
# ERROR RESPONSE SCHEMAS
# ================================

class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ValidationErrorResponse(BaseModel):
    """Validation error response"""
    error: str = "validation_error"
    message: str
    field_errors: Dict[str, List[str]]
    timestamp: datetime = Field(default_factory=datetime.now)
