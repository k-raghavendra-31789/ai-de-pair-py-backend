"""
Database Models for AI SQL Generation System
===========================================

Core SQLAlchemy models for session management, Excel analysis,
AI interactions, and SQL generation results.
"""

from sqlalchemy import Column, String, Text, DateTime, Enum, Integer, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum
import uuid
from datetime import datetime
from typing import Optional


# ================================
# ENUMS FOR STATUS TRACKING
# ================================

class SessionStatus(enum.Enum):
    """Status of an analysis session"""
    CREATED = "created"
    PROCESSING_EXCEL = "processing_excel"
    DISCOVERY_QUESTIONS = "discovery_questions"
    AWAITING_USER_INPUT = "awaiting_user_input"
    STRATEGIC_CLARIFICATION = "strategic_clarification"
    GENERATING_SQL = "generating_sql"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class QuestionType(enum.Enum):
    """Type of AI question asked to user"""
    INFORMATION_DISCOVERY = "information_discovery"
    STRATEGIC_CLARIFICATION = "strategic_clarification"
    TRANSFORMATION_STRATEGY = "transformation_strategy"
    JOIN_STRATEGY = "join_strategy"
    OUTPUT_FORMAT = "output_format"
    MULTI_TABLE_DETECTION = "multi_table_detection"


class SQLGenerationStrategy(enum.Enum):
    """Strategy used for SQL generation"""
    SINGLE_UNIFIED_QUERY = "single_unified_query"
    MULTIPLE_SEPARATE_QUERIES = "multiple_separate_queries"
    SEQUENTIAL_PIPELINE = "sequential_pipeline"


class ValidationStatus(enum.Enum):
    """Status of SQL validation"""
    PASSED = "passed"
    FAILED = "failed"
    WARNINGS = "warnings"
    NOT_VALIDATED = "not_validated"


# ================================
# CORE MODELS
# ================================

class AnalysisSession(Base):
    """
    Main session tracking for each Excel analysis workflow.
    
    Tracks the complete journey from Excel upload through SQL generation.
    """
    __tablename__ = "analysis_sessions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(Enum(SessionStatus), default=SessionStatus.CREATED, nullable=False)
    
    # Session metadata
    filename = Column(String, nullable=True)  # Original Excel filename
    file_hash = Column(String, nullable=True)  # Hash of Excel content for deduplication
    user_id = Column(String, nullable=True)  # Optional user identification
    
    # Progress tracking
    current_phase = Column(String, nullable=True)  # Current processing phase
    progress_percentage = Column(Float, default=0.0)  # Overall progress (0-100)
    
    # Configuration
    ai_provider = Column(String, default="openai")  # AI provider used
    connection_details = Column(JSON, nullable=True)  # Database connection info
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    
    # Error tracking
    error_message = Column(Text, nullable=True)
    error_trace = Column(Text, nullable=True)
    
    # Relationships
    excel_documents = relationship("ExcelDocument", back_populates="session", cascade="all, delete-orphan")
    ai_interactions = relationship("AIInteraction", back_populates="session", cascade="all, delete-orphan")
    sql_generations = relationship("SQLGeneration", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<AnalysisSession(id={self.id}, status={self.status.value}, filename={self.filename})>"


class ExcelDocument(Base):
    """
    Excel file analysis and caching.
    
    Stores processed Excel content to avoid re-analyzing identical files.
    """
    __tablename__ = "excel_documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("analysis_sessions.id"), nullable=False)
    
    # File information
    filename = Column(String, nullable=False)
    file_hash = Column(String, nullable=False, index=True)  # For deduplication
    file_size = Column(Integer, nullable=True)
    
    # Excel structure analysis
    sheet_count = Column(Integer, nullable=False)
    sheet_names = Column(JSON, nullable=False)  # List of sheet names
    
    # Content analysis results
    sheet_analysis = Column(JSON, nullable=True)  # Per-sheet pattern analysis
    information_mapping = Column(JSON, nullable=True)  # Where key info was found
    discovered_patterns = Column(JSON, nullable=True)  # Detected content patterns
    
    # Processing metadata
    processing_time_seconds = Column(Float, nullable=True)
    ai_confidence_score = Column(Float, nullable=True)  # AI's confidence in analysis
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    session = relationship("AnalysisSession", back_populates="excel_documents")
    
    def __repr__(self):
        return f"<ExcelDocument(id={self.id}, filename={self.filename}, sheets={self.sheet_count})>"


class AIInteraction(Base):
    """
    AI question and user response tracking.
    
    Stores all strategic questions asked by AI and user responses
    for context building and session resume capability.
    """
    __tablename__ = "ai_interactions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("analysis_sessions.id"), nullable=False)
    
    # Question details
    question_type = Column(Enum(QuestionType), nullable=False)
    question_text = Column(Text, nullable=False)
    question_context = Column(Text, nullable=True)  # Additional context for the question
    question_options = Column(JSON, nullable=True)  # Multiple choice options if applicable
    
    # User response
    user_response = Column(JSON, nullable=True)  # User's answer/selection
    response_text = Column(Text, nullable=True)  # Free-text response if applicable
    confidence_level = Column(Float, nullable=True)  # AI's confidence in interpretation
    
    # Metadata
    priority = Column(String, nullable=True)  # high, medium, low
    sequence_number = Column(Integer, nullable=True)  # Order of questions in session
    
    # Processing results
    ai_interpretation = Column(JSON, nullable=True)  # How AI interpreted the response
    impact_on_sql = Column(Text, nullable=True)  # How this affects SQL generation
    
    # Timestamps
    asked_at = Column(DateTime, default=func.now(), nullable=False)
    answered_at = Column(DateTime, nullable=True)
    
    # Relationships
    session = relationship("AnalysisSession", back_populates="ai_interactions")
    
    def __repr__(self):
        return f"<AIInteraction(id={self.id}, type={self.question_type.value}, answered={self.answered_at is not None})>"


class SQLGeneration(Base):
    """
    Generated SQL storage and versioning.
    
    Stores all SQL generation attempts, iterations, and validation results.
    """
    __tablename__ = "sql_generations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("analysis_sessions.id"), nullable=False)
    
    # Generation strategy
    generation_strategy = Column(Enum(SQLGenerationStrategy), nullable=False)
    version = Column(Integer, default=1, nullable=False)  # Track iterations
    
    # SQL content
    sql_content = Column(Text, nullable=False)
    sql_explanation = Column(Text, nullable=True)  # AI's explanation of the SQL
    target_tables = Column(JSON, nullable=True)  # List of target tables generated
    
    # Validation and analysis
    validation_status = Column(Enum(ValidationStatus), default=ValidationStatus.NOT_VALIDATED)
    validation_errors = Column(JSON, nullable=True)  # List of validation errors
    validation_warnings = Column(JSON, nullable=True)  # List of warnings
    
    # Performance analysis
    estimated_complexity = Column(String, nullable=True)  # simple, medium, complex
    estimated_execution_time = Column(Float, nullable=True)  # Estimated seconds
    query_optimization_notes = Column(Text, nullable=True)
    
    # AI generation metadata
    ai_provider_used = Column(String, nullable=False)
    token_usage_input = Column(Integer, nullable=True)
    token_usage_output = Column(Integer, nullable=True)
    generation_time_seconds = Column(Float, nullable=True)
    cost_estimate = Column(Float, nullable=True)  # Estimated API cost
    
    # User feedback
    user_rating = Column(Integer, nullable=True)  # 1-5 rating
    user_feedback = Column(Text, nullable=True)
    
    # Timestamps
    generated_at = Column(DateTime, default=func.now(), nullable=False)
    validated_at = Column(DateTime, nullable=True)
    
    # Relationships
    session = relationship("AnalysisSession", back_populates="sql_generations")
    
    def __repr__(self):
        return f"<SQLGeneration(id={self.id}, strategy={self.generation_strategy.value}, version={self.version})>"


class AIMemoryCache(Base):
    """
    Local AI memory for cost optimization.
    
    Stores vector embeddings and cached AI responses to reduce API calls
    as specified in the requirements for cost optimization.
    """
    __tablename__ = "ai_memory_cache"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Content identification
    content_hash = Column(String, nullable=False, unique=True, index=True)
    content_type = Column(String, nullable=False)  # excel_analysis, sql_generation, etc.
    
    # AI provider and model info
    ai_provider = Column(String, nullable=False)
    model_name = Column(String, nullable=True)
    
    # Cached content
    input_content = Column(Text, nullable=False)
    cached_response = Column(JSON, nullable=False)
    vector_embedding = Column(JSON, nullable=True)  # Sentence transformer embedding
    
    # Usage statistics
    cache_hits = Column(Integer, default=0)
    last_used_at = Column(DateTime, default=func.now())
    
    # Cost tracking
    original_token_count = Column(Integer, nullable=True)
    estimated_cost_saved = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=True)  # Optional expiration
    
    def __repr__(self):
        return f"<AIMemoryCache(id={self.id}, type={self.content_type}, hits={self.cache_hits})>"
