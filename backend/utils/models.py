"""
Data models for Excel-based SQL generation requests
"""
from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class ExcelSheetData(BaseModel):
    """Represents data from a single Excel sheet"""
    name: str
    rows: List[List[Any]]  # 2D array of cell values
    headers: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ExcelMappingRequest(BaseModel):
    """Request model for Excel-based SQL generation"""
    sheets: List[ExcelSheetData]  # All sheets from the Excel file
    filename: Optional[str] = None
    ai_api_key: str
    ai_provider: str = "openai"
    connection_details: Optional[Dict[str, str]] = None
    additional_context: Optional[str] = None  # Any extra context from user
