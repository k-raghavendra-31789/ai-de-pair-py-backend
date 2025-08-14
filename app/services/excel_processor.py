"""
Excel Content Processing Service for Phase 2
============================================

Handles the processing of Excel content received from frontend.
Analyzes business logic, patterns, and prepares for AI processing.
"""

import uuid
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from app.schemas import ExcelContentPayload, ExcelProcessingResponse, ExcelProcessingStatus
from app.db.models import AnalysisSession, ExcelDocument
import json
import logging

logger = logging.getLogger(__name__)


class ExcelContentProcessor:
    """Process Excel content and extract business intelligence"""
    
    def __init__(self, db: Session):
        self.db = db
        self.processing_jobs: Dict[str, ExcelProcessingStatus] = {}
    
    async def process_excel_content(self, payload: ExcelContentPayload) -> ExcelProcessingResponse:
        """
        Main entry point for Excel content processing
        
        Args:
            payload: Excel content from frontend
            
        Returns:
            Processing response with job ID
        """
        job_id = str(uuid.uuid4())
        
        # Validate session exists
        session = self.db.query(AnalysisSession).filter(
            AnalysisSession.id == payload.session_id
        ).first()
        
        if not session:
            raise ValueError(f"Session {payload.session_id} not found")
        
        # Calculate content size
        total_cells = sum(
            len(row) for sheet in payload.sheets 
            for row in sheet.content
        )
        
        # Create processing status
        processing_status = ExcelProcessingStatus(
            job_id=job_id,
            session_id=payload.session_id,
            status="processing",
            progress_percentage=0,
            current_step="Initializing content analysis",
            started_at=datetime.now()
        )
        
        self.processing_jobs[job_id] = processing_status
        
        # Start background processing
        asyncio.create_task(self._process_content_background(job_id, payload, session))
        
        return ExcelProcessingResponse(
            job_id=job_id,
            session_id=payload.session_id,
            sheets_received=len(payload.sheets),
            total_content_size=total_cells
        )
    
    async def _process_content_background(
        self, 
        job_id: str, 
        payload: ExcelContentPayload, 
        session: AnalysisSession
    ):
        """Background processing of Excel content"""
        try:
            processing_status = self.processing_jobs[job_id]
            
            # Step 1: Store raw content
            processing_status.current_step = "Storing raw Excel content"
            processing_status.progress_percentage = 10
            
            excel_doc = await self._store_raw_content(payload, session)
            
            # Step 2: Analyze sheet patterns
            processing_status.current_step = "Analyzing sheet patterns and structure"
            processing_status.progress_percentage = 30
            
            patterns = await self._analyze_sheet_patterns(payload.sheets)
            processing_status.patterns_detected = patterns
            
            # Step 3: Extract business logic
            processing_status.current_step = "Extracting business logic and requirements"
            processing_status.progress_percentage = 50
            
            business_logic = await self._extract_business_logic(payload.sheets)
            processing_status.business_logic_found = business_logic
            
            # Step 4: Detect table mappings
            processing_status.current_step = "Identifying table and column mappings"
            processing_status.progress_percentage = 70
            
            table_mappings = await self._detect_table_mappings(payload.sheets)
            processing_status.table_mappings_discovered = table_mappings
            
            # Step 5: Prepare AI-ready content
            processing_status.current_step = "Preparing content for AI analysis"
            processing_status.progress_percentage = 90
            
            ai_ready_content = await self._prepare_ai_content(payload, patterns, business_logic, table_mappings)
            
            # Step 6: Update database with processed content
            await self._update_excel_document(excel_doc, ai_ready_content, patterns)
            
            # Update session status
            session.status = "processing_excel"
            session.current_phase = "excel_analysis"
            session.progress_percentage = 25.0  # Phase 2 is 25% of total
            self.db.commit()
            
            # Complete processing
            processing_status.status = "completed"
            processing_status.current_step = "Content processing completed successfully"
            processing_status.progress_percentage = 100
            processing_status.completed_at = datetime.now()
            
            logger.info(f"Excel content processing completed for job {job_id}")
            
        except Exception as e:
            logger.error(f"Excel processing failed for job {job_id}: {str(e)}")
            processing_status.status = "failed"
            processing_status.error_message = str(e)
            processing_status.completed_at = datetime.now()
    
    async def _store_raw_content(self, payload: ExcelContentPayload, session: AnalysisSession) -> ExcelDocument:
        """Store raw Excel content in database"""
        
        # Create or update ExcelDocument
        excel_doc = self.db.query(ExcelDocument).filter(
            ExcelDocument.session_id == session.id
        ).first()
        
        # Convert payload to JSON-serializable format
        payload_dict = payload.dict()
        # Convert datetime to ISO string
        if 'file_metadata' in payload_dict and 'upload_timestamp' in payload_dict['file_metadata']:
            payload_dict['file_metadata']['upload_timestamp'] = payload_dict['file_metadata']['upload_timestamp'].isoformat()
        
        if not excel_doc:
            excel_doc = ExcelDocument(
                id=str(uuid.uuid4()),
                session_id=session.id,
                filename=payload.file_metadata.filename,
                file_hash="placeholder_hash",  # TODO: Generate actual hash
                file_size=int((payload.file_metadata.file_size_mb or 0.0) * 1024 * 1024),  # Convert MB to bytes
                sheet_count=len(payload.sheets),
                sheet_names=[sheet.sheet_name for sheet in payload.sheets],
                sheet_analysis=payload_dict,  # Store complete payload as JSON
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            self.db.add(excel_doc)
        else:
            excel_doc.sheet_analysis = payload_dict
            excel_doc.updated_at = datetime.now()
        
        self.db.commit()
        return excel_doc
    
    async def _analyze_sheet_patterns(self, sheets: List) -> Dict[str, Any]:
        """Analyze patterns in Excel sheets"""
        patterns = {
            "sheet_types": {},
            "content_patterns": [],
            "structure_analysis": {}
        }
        
        for sheet in sheets:
            sheet_analysis = {
                "name": sheet.sheet_name,
                "row_count": len(sheet.content),
                "column_count": max(len(row) for row in sheet.content) if sheet.content else 0,
                "has_headers": False,
                "table_like": False,
                "text_heavy": False
            }
            
            if sheet.content:
                # Check if first row looks like headers
                first_row = sheet.content[0] if sheet.content else []
                if first_row and all(isinstance(cell, str) and cell.strip() for cell in first_row):
                    sheet_analysis["has_headers"] = True
                
                # Check if content is table-like
                if len(sheet.content) > 2:
                    consistent_columns = all(
                        len(row) == len(sheet.content[0]) 
                        for row in sheet.content[:5]  # Check first 5 rows
                    )
                    sheet_analysis["table_like"] = consistent_columns
                
                # Check if content is text-heavy
                text_cells = sum(
                    1 for row in sheet.content 
                    for cell in row 
                    if isinstance(cell, str) and len(cell) > 20
                )
                sheet_analysis["text_heavy"] = text_cells > len(sheet.content) * 0.3
            
            patterns["sheet_types"][sheet.sheet_name] = sheet_analysis
        
        return patterns
    
    async def _extract_business_logic(self, sheets: List) -> List[str]:
        """Extract business logic and requirements from sheet content"""
        business_logic = []
        
        # Keywords that indicate business logic
        business_keywords = [
            "calculate", "sum", "total", "average", "count", "group by",
            "join", "where", "filter", "exclude", "include", "only",
            "active", "inactive", "status", "date range", "period",
            "rule", "requirement", "condition", "criteria", "logic"
        ]
        
        for sheet in sheets:
            for row_idx, row in enumerate(sheet.content):
                for cell_idx, cell in enumerate(row):
                    if isinstance(cell, str) and len(cell) > 10:
                        cell_lower = cell.lower()
                        if any(keyword in cell_lower for keyword in business_keywords):
                            business_logic.append({
                                "sheet": sheet.sheet_name,
                                "row": row_idx + 1,
                                "column": cell_idx + 1,
                                "text": cell,
                                "type": "business_rule"
                            })
        
        return business_logic
    
    async def _detect_table_mappings(self, sheets: List) -> List[str]:
        """Detect table and column mappings"""
        mappings = []
        
        # Look for mapping patterns
        mapping_indicators = [
            "source", "target", "table", "column", "field",
            "from", "to", "mapping", "map", "transform"
        ]
        
        for sheet in sheets:
            # Check if this sheet contains mapping information
            sheet_has_mappings = False
            
            for row in sheet.content[:5]:  # Check first 5 rows for headers
                if any(
                    isinstance(cell, str) and 
                    any(indicator in cell.lower() for indicator in mapping_indicators)
                    for cell in row
                ):
                    sheet_has_mappings = True
                    break
            
            if sheet_has_mappings:
                mappings.append({
                    "sheet": sheet.sheet_name,
                    "type": "table_mapping",
                    "confidence": "medium",
                    "description": f"Sheet '{sheet.sheet_name}' appears to contain table/column mappings"
                })
        
        return mappings
    
    async def _prepare_ai_content(
        self, 
        payload: ExcelContentPayload, 
        patterns: Dict[str, Any],
        business_logic: List[str],
        table_mappings: List[str]
    ) -> Dict[str, Any]:
        """Prepare content for AI processing"""
        
        ai_content = {
            "source_filename": payload.file_metadata.filename,
            "processing_timestamp": datetime.now().isoformat(),
            "sheet_analysis": patterns,
            "business_requirements": business_logic,
            "table_mappings": table_mappings,
            "consolidated_text": self._create_consolidated_text(payload.sheets),
            "processing_metadata": {
                "total_sheets": len(payload.sheets),
                "total_rows": sum(len(sheet.content) for sheet in payload.sheets),
                "analysis_confidence": "medium",
                "next_phase": "information_discovery"
            }
        }
        
        return ai_content
    
    def _create_consolidated_text(self, sheets: List) -> str:
        """Create consolidated text representation for AI"""
        text_parts = [
            "EXCEL MAPPING DOCUMENT ANALYSIS",
            "=" * 50,
            ""
        ]
        
        for sheet in sheets:
            text_parts.extend([
                f"SHEET: {sheet.sheet_name}",
                f"Rows: {len(sheet.content)}",
                ""
            ])
            
            # Add content (limit to prevent overwhelming AI)
            for i, row in enumerate(sheet.content[:20]):  # First 20 rows
                row_text = " | ".join(str(cell) for cell in row if cell and str(cell).strip())
                if row_text:
                    text_parts.append(f"  Row {i+1}: {row_text}")
            
            if len(sheet.content) > 20:
                text_parts.append(f"  ... and {len(sheet.content) - 20} more rows")
            
            text_parts.append("")
        
        return "\n".join(text_parts)
    
    async def _update_excel_document(
        self, 
        excel_doc: ExcelDocument, 
        ai_content: Dict[str, Any],
        patterns: Dict[str, Any]
    ):
        """Update Excel document with processed content"""
        
        excel_doc.information_mapping = ai_content
        excel_doc.discovered_patterns = patterns
        excel_doc.ai_confidence_score = 0.8  # Default confidence score
        excel_doc.updated_at = datetime.now()
        
        self.db.commit()
    
    def get_processing_status(self, job_id: str) -> Optional[ExcelProcessingStatus]:
        """Get processing status for a job"""
        return self.processing_jobs.get(job_id)
    
    def get_session_excel_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get processed Excel data for a session"""
        excel_doc = self.db.query(ExcelDocument).filter(
            ExcelDocument.session_id == session_id
        ).first()
        
        if excel_doc and excel_doc.information_mapping:
            return excel_doc.information_mapping
        
        return None
