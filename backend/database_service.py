"""
Database Service Functions
==========================

Service layer for database operations in the AI SQL generation system.
Provides clean interface for CRUD operations on all models.
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import hashlib
import json

from models import (
    AnalysisSession, ExcelDocument, AIInteraction, SQLGeneration, AIMemoryCache,
    SessionStatus, QuestionType, SQLGenerationStrategy, ValidationStatus
)
from schemas import CreateSessionRequest, UserResponseRequest


# ================================
# SESSION MANAGEMENT
# ================================

class SessionService:
    """Service for managing analysis sessions"""
    
    @staticmethod
    def create_session(db: Session, request: CreateSessionRequest) -> AnalysisSession:
        """Create a new analysis session"""
        session = AnalysisSession(
            id=str(uuid.uuid4()),
            filename=request.filename,
            user_id=request.user_id,
            ai_provider=request.ai_provider,
            connection_details=request.connection_details,
            status=SessionStatus.CREATED
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_session(db: Session, session_id: str) -> Optional[AnalysisSession]:
        """Get session by ID"""
        return db.query(AnalysisSession).filter(AnalysisSession.id == session_id).first()
    
    @staticmethod
    def update_session_status(
        db: Session, 
        session_id: str, 
        status: SessionStatus, 
        current_phase: Optional[str] = None,
        progress_percentage: Optional[float] = None,
        error_message: Optional[str] = None
    ) -> Optional[AnalysisSession]:
        """Update session status and progress"""
        session = db.query(AnalysisSession).filter(AnalysisSession.id == session_id).first()
        if not session:
            return None
        
        session.status = status
        if current_phase:
            session.current_phase = current_phase
        if progress_percentage is not None:
            session.progress_percentage = progress_percentage
        if error_message:
            session.error_message = error_message
        if status == SessionStatus.COMPLETED:
            session.completed_at = datetime.now()
        
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_recent_sessions(db: Session, limit: int = 10) -> List[AnalysisSession]:
        """Get recent sessions ordered by creation date"""
        return db.query(AnalysisSession)\
                 .order_by(desc(AnalysisSession.created_at))\
                 .limit(limit)\
                 .all()
    
    @staticmethod
    def get_sessions_by_status(db: Session, status: SessionStatus) -> List[AnalysisSession]:
        """Get all sessions with specific status"""
        return db.query(AnalysisSession)\
                 .filter(AnalysisSession.status == status)\
                 .order_by(desc(AnalysisSession.created_at))\
                 .all()


# ================================
# EXCEL DOCUMENT MANAGEMENT
# ================================

class ExcelDocumentService:
    """Service for managing Excel document analysis"""
    
    @staticmethod
    def create_excel_document(
        db: Session,
        session_id: str,
        filename: str,
        file_content: bytes,
        sheet_names: List[str],
        sheet_analysis: Optional[Dict[str, Any]] = None
    ) -> ExcelDocument:
        """Create Excel document record with analysis"""
        
        # Generate file hash for deduplication
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        excel_doc = ExcelDocument(
            id=str(uuid.uuid4()),
            session_id=session_id,
            filename=filename,
            file_hash=file_hash,
            file_size=len(file_content),
            sheet_count=len(sheet_names),
            sheet_names=sheet_names,
            sheet_analysis=sheet_analysis
        )
        
        db.add(excel_doc)
        db.commit()
        db.refresh(excel_doc)
        return excel_doc
    
    @staticmethod
    def update_analysis_results(
        db: Session,
        document_id: str,
        sheet_analysis: Dict[str, Any],
        information_mapping: Dict[str, Any],
        discovered_patterns: Dict[str, Any],
        processing_time: float,
        confidence_score: float
    ) -> Optional[ExcelDocument]:
        """Update Excel document with analysis results"""
        
        excel_doc = db.query(ExcelDocument).filter(ExcelDocument.id == document_id).first()
        if not excel_doc:
            return None
        
        excel_doc.sheet_analysis = sheet_analysis
        excel_doc.information_mapping = information_mapping
        excel_doc.discovered_patterns = discovered_patterns
        excel_doc.processing_time_seconds = processing_time
        excel_doc.ai_confidence_score = confidence_score
        
        db.commit()
        db.refresh(excel_doc)
        return excel_doc
    
    @staticmethod
    def find_by_file_hash(db: Session, file_hash: str) -> Optional[ExcelDocument]:
        """Find Excel document by file hash for deduplication"""
        return db.query(ExcelDocument).filter(ExcelDocument.file_hash == file_hash).first()
    
    @staticmethod
    def get_session_documents(db: Session, session_id: str) -> List[ExcelDocument]:
        """Get all Excel documents for a session"""
        return db.query(ExcelDocument)\
                 .filter(ExcelDocument.session_id == session_id)\
                 .order_by(ExcelDocument.created_at)\
                 .all()


# ================================
# AI INTERACTION MANAGEMENT
# ================================

class AIInteractionService:
    """Service for managing AI questions and user responses"""
    
    @staticmethod
    def create_question(
        db: Session,
        session_id: str,
        question_type: QuestionType,
        question_text: str,
        question_context: Optional[str] = None,
        question_options: Optional[List[Dict[str, Any]]] = None,
        priority: str = "medium",
        sequence_number: Optional[int] = None
    ) -> AIInteraction:
        """Create a new AI question"""
        
        # Auto-generate sequence number if not provided
        if sequence_number is None:
            last_interaction = db.query(AIInteraction)\
                                .filter(AIInteraction.session_id == session_id)\
                                .order_by(desc(AIInteraction.sequence_number))\
                                .first()
            sequence_number = (last_interaction.sequence_number + 1) if last_interaction else 1
        
        interaction = AIInteraction(
            id=str(uuid.uuid4()),
            session_id=session_id,
            question_type=question_type,
            question_text=question_text,
            question_context=question_context,
            question_options=question_options,
            priority=priority,
            sequence_number=sequence_number
        )
        
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return interaction
    
    @staticmethod
    def submit_response(
        db: Session,
        interaction_id: str,
        user_response: Dict[str, Any],
        response_text: Optional[str] = None,
        confidence_level: Optional[float] = None,
        ai_interpretation: Optional[Dict[str, Any]] = None
    ) -> Optional[AIInteraction]:
        """Submit user response to AI question"""
        
        interaction = db.query(AIInteraction).filter(AIInteraction.id == interaction_id).first()
        if not interaction:
            return None
        
        interaction.user_response = user_response
        interaction.response_text = response_text
        interaction.confidence_level = confidence_level
        interaction.ai_interpretation = ai_interpretation
        interaction.answered_at = datetime.now()
        
        db.commit()
        db.refresh(interaction)
        return interaction
    
    @staticmethod
    def get_session_interactions(db: Session, session_id: str) -> List[AIInteraction]:
        """Get all interactions for a session"""
        return db.query(AIInteraction)\
                 .filter(AIInteraction.session_id == session_id)\
                 .order_by(AIInteraction.sequence_number)\
                 .all()
    
    @staticmethod
    def get_unanswered_questions(db: Session, session_id: str) -> List[AIInteraction]:
        """Get unanswered questions for a session"""
        return db.query(AIInteraction)\
                 .filter(
                     AIInteraction.session_id == session_id,
                     AIInteraction.answered_at.is_(None)
                 )\
                 .order_by(AIInteraction.sequence_number)\
                 .all()


# ================================
# SQL GENERATION MANAGEMENT
# ================================

class SQLGenerationService:
    """Service for managing SQL generation results"""
    
    @staticmethod
    def create_sql_generation(
        db: Session,
        session_id: str,
        generation_strategy: SQLGenerationStrategy,
        sql_content: str,
        ai_provider: str,
        sql_explanation: Optional[str] = None,
        target_tables: Optional[List[str]] = None,
        token_usage_input: Optional[int] = None,
        token_usage_output: Optional[int] = None,
        generation_time: Optional[float] = None,
        cost_estimate: Optional[float] = None
    ) -> SQLGeneration:
        """Create a new SQL generation record"""
        
        # Get next version number for this session
        last_generation = db.query(SQLGeneration)\
                           .filter(SQLGeneration.session_id == session_id)\
                           .order_by(desc(SQLGeneration.version))\
                           .first()
        version = (last_generation.version + 1) if last_generation else 1
        
        sql_gen = SQLGeneration(
            id=str(uuid.uuid4()),
            session_id=session_id,
            generation_strategy=generation_strategy,
            version=version,
            sql_content=sql_content,
            sql_explanation=sql_explanation,
            target_tables=target_tables,
            ai_provider_used=ai_provider,
            token_usage_input=token_usage_input,
            token_usage_output=token_usage_output,
            generation_time_seconds=generation_time,
            cost_estimate=cost_estimate
        )
        
        db.add(sql_gen)
        db.commit()
        db.refresh(sql_gen)
        return sql_gen
    
    @staticmethod
    def update_validation_results(
        db: Session,
        generation_id: str,
        validation_status: ValidationStatus,
        validation_errors: Optional[List[str]] = None,
        validation_warnings: Optional[List[str]] = None,
        estimated_complexity: Optional[str] = None,
        estimated_execution_time: Optional[float] = None
    ) -> Optional[SQLGeneration]:
        """Update SQL generation with validation results"""
        
        sql_gen = db.query(SQLGeneration).filter(SQLGeneration.id == generation_id).first()
        if not sql_gen:
            return None
        
        sql_gen.validation_status = validation_status
        sql_gen.validation_errors = validation_errors
        sql_gen.validation_warnings = validation_warnings
        sql_gen.estimated_complexity = estimated_complexity
        sql_gen.estimated_execution_time = estimated_execution_time
        sql_gen.validated_at = datetime.now()
        
        db.commit()
        db.refresh(sql_gen)
        return sql_gen
    
    @staticmethod
    def get_session_generations(db: Session, session_id: str) -> List[SQLGeneration]:
        """Get all SQL generations for a session"""
        return db.query(SQLGeneration)\
                 .filter(SQLGeneration.session_id == session_id)\
                 .order_by(desc(SQLGeneration.version))\
                 .all()
    
    @staticmethod
    def get_latest_generation(db: Session, session_id: str) -> Optional[SQLGeneration]:
        """Get the latest SQL generation for a session"""
        return db.query(SQLGeneration)\
                 .filter(SQLGeneration.session_id == session_id)\
                 .order_by(desc(SQLGeneration.version))\
                 .first()


# ================================
# AI MEMORY CACHE MANAGEMENT
# ================================

class AIMemoryCacheService:
    """Service for managing AI memory cache for cost optimization"""
    
    @staticmethod
    def store_cache(
        db: Session,
        content: str,
        content_type: str,
        ai_provider: str,
        cached_response: Dict[str, Any],
        model_name: Optional[str] = None,
        vector_embedding: Optional[List[float]] = None,
        token_count: Optional[int] = None,
        expires_hours: Optional[int] = None
    ) -> AIMemoryCache:
        """Store content in AI memory cache"""
        
        # Generate content hash
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Calculate expiration if specified
        expires_at = None
        if expires_hours:
            expires_at = datetime.now() + timedelta(hours=expires_hours)
        
        cache_entry = AIMemoryCache(
            id=str(uuid.uuid4()),
            content_hash=content_hash,
            content_type=content_type,
            ai_provider=ai_provider,
            model_name=model_name,
            input_content=content,
            cached_response=cached_response,
            vector_embedding=vector_embedding,
            original_token_count=token_count,
            expires_at=expires_at
        )
        
        db.add(cache_entry)
        db.commit()
        db.refresh(cache_entry)
        return cache_entry
    
    @staticmethod
    def get_cached_response(
        db: Session,
        content: str,
        content_type: str,
        ai_provider: str
    ) -> Optional[AIMemoryCache]:
        """Retrieve cached response if available"""
        
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        cache_entry = db.query(AIMemoryCache)\
                       .filter(
                           AIMemoryCache.content_hash == content_hash,
                           AIMemoryCache.content_type == content_type,
                           AIMemoryCache.ai_provider == ai_provider
                       )\
                       .filter(
                           # Check expiration
                           db.or_(
                               AIMemoryCache.expires_at.is_(None),
                               AIMemoryCache.expires_at > datetime.now()
                           )
                       )\
                       .first()
        
        if cache_entry:
            # Update usage statistics
            cache_entry.cache_hits += 1
            cache_entry.last_used_at = datetime.now()
            db.commit()
        
        return cache_entry
    
    @staticmethod
    def cleanup_expired_cache(db: Session) -> int:
        """Remove expired cache entries"""
        expired_count = db.query(AIMemoryCache)\
                         .filter(
                             AIMemoryCache.expires_at.isnot(None),
                             AIMemoryCache.expires_at < datetime.now()
                         )\
                         .delete()
        db.commit()
        return expired_count
    
    @staticmethod
    def get_cache_statistics(db: Session) -> Dict[str, Any]:
        """Get cache usage statistics"""
        stats = {
            "total_entries": db.query(AIMemoryCache).count(),
            "total_hits": db.query(func.sum(AIMemoryCache.cache_hits)).scalar() or 0,
            "total_cost_saved": db.query(func.sum(AIMemoryCache.estimated_cost_saved)).scalar() or 0.0
        }
        
        # Get stats by provider
        provider_stats = db.query(
            AIMemoryCache.ai_provider,
            func.count(AIMemoryCache.id).label('entry_count'),
            func.sum(AIMemoryCache.cache_hits).label('total_hits')
        ).group_by(AIMemoryCache.ai_provider).all()
        
        stats["by_provider"] = {
            provider: {"entries": count, "hits": hits}
            for provider, count, hits in provider_stats
        }
        
        return stats
