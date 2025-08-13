"""
Excel data processor for handling parsed Excel content from frontend
"""
from typing import Dict, List, Any
from utils.models import ExcelSheetData, ExcelMappingRequest


class ExcelDataProcessor:
    """
    Process Excel data that's already been parsed on the frontend
    Convert it to a format suitable for AI analysis
    """
    
    def __init__(self):
        self.processed_data = {}
    
    def process_excel_request(self, excel_request: ExcelMappingRequest) -> str:
        """
        Convert Excel request data into a comprehensive text representation for AI
        
        Args:
            excel_request: Parsed Excel data from frontend
            
        Returns:
            Consolidated text representation for AI processing
        """
        text_parts = [
            "EXCEL MAPPING DOCUMENT ANALYSIS",
            "=" * 50,
            ""
        ]
        
        # Add metadata
        if excel_request.filename:
            text_parts.append(f"FILENAME: {excel_request.filename}")
        
        text_parts.extend([
            f"TOTAL SHEETS: {len(excel_request.sheets)}",
            f"SHEET NAMES: {', '.join([sheet.name for sheet in excel_request.sheets])}",
            ""
        ])
        
        # Add additional context if provided
        if excel_request.additional_context:
            text_parts.extend([
                "USER PROVIDED CONTEXT:",
                excel_request.additional_context,
                ""
            ])
        
        # Process each sheet
        for sheet in excel_request.sheets:
            sheet_text = self._process_sheet(sheet)
            text_parts.extend([
                f"{'='*20} SHEET: {sheet.name} {'='*20}",
                sheet_text,
                "",
                "-" * 50,
                ""
            ])
        
        return "\n".join(text_parts)
    
    def _process_sheet(self, sheet: ExcelSheetData) -> str:
        """Process a single sheet into text representation"""
        text_parts = [
            f"SHEET NAME: {sheet.name}",
            f"TOTAL ROWS: {len(sheet.rows)}",
            ""
        ]
        
        # Add headers if available
        if sheet.headers:
            text_parts.extend([
                "IDENTIFIED HEADERS:",
                " | ".join(sheet.headers),
                ""
            ])
        
        # Add metadata if available
        if sheet.metadata:
            text_parts.extend([
                "SHEET METADATA:",
                str(sheet.metadata),
                ""
            ])
        
        # Process rows and identify patterns
        if sheet.rows:
            text_parts.append("ROW DATA:")
            
            # Show first few rows for context
            for i, row in enumerate(sheet.rows[:10]):  # Limit to first 10 rows
                # Convert row to strings and filter empty cells
                row_data = [str(cell) for cell in row if cell is not None and str(cell).strip()]
                if row_data:  # Only show rows with actual data
                    text_parts.append(f"  Row {i+1}: {' | '.join(row_data)}")
            
            if len(sheet.rows) > 10:
                text_parts.append(f"  ... and {len(sheet.rows) - 10} more rows")
            
            text_parts.append("")
            
            # Identify potential table structures
            table_analysis = self._analyze_table_structure(sheet.rows)
            if table_analysis:
                text_parts.extend([
                    "TABLE STRUCTURE ANALYSIS:",
                    table_analysis,
                    ""
                ])
            
            # Extract all unique text values for AI context
            all_text = self._extract_all_text(sheet.rows)
            if all_text:
                text_parts.extend([
                    "ALL UNIQUE TEXT VALUES:",
                    ", ".join(all_text[:50]),  # Limit to first 50 unique values
                    ""
                ])
        
        return "\n".join(text_parts)
    
    def _analyze_table_structure(self, rows: List[List[Any]]) -> str:
        """Analyze the structure of rows to identify potential tables"""
        if not rows:
            return ""
        
        analysis_parts = []
        
        # Check for header rows (first row with text, subsequent rows with data)
        if len(rows) > 1:
            first_row = [str(cell) for cell in rows[0] if cell is not None]
            if first_row and all(isinstance(cell, str) for cell in first_row if cell):
                analysis_parts.append(f"Potential header row detected: {' | '.join(first_row)}")
        
        # Count columns with data
        max_cols = max(len(row) for row in rows) if rows else 0
        col_data_count = [0] * max_cols
        
        for row in rows:
            for i, cell in enumerate(row):
                if i < max_cols and cell is not None and str(cell).strip():
                    col_data_count[i] += 1
        
        active_columns = [i for i, count in enumerate(col_data_count) if count > 0]
        if active_columns:
            analysis_parts.append(f"Active columns: {len(active_columns)} out of {max_cols}")
            analysis_parts.append(f"Column usage: {col_data_count[:10]}")  # Show first 10 columns
        
        return "\n".join(analysis_parts)
    
    def _extract_all_text(self, rows: List[List[Any]]) -> List[str]:
        """Extract all unique text values from rows"""
        all_text = set()
        
        for row in rows:
            for cell in row:
                if cell is not None:
                    text = str(cell).strip()
                    if text and len(text) > 1:  # Filter out single characters and empty strings
                        all_text.add(text)
        
        # Sort by length and relevance (longer text first, then alphabetically)
        return sorted(list(all_text), key=lambda x: (-len(x), x.lower()))
