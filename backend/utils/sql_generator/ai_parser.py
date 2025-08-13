"""
AI-powered input parser using raw HTTP requests to LLM APIs
"""
import json
import asyncio
import aiohttp
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ParsedMapping:
    """Normalized structure extracted by AI from raw input"""
    tables: list
    relationships: list
    output_columns: list
    filters: list
    business_logic: list
    connection_details: dict
    metadata: dict


class AIInputParser:
    """
    AI-powered parser that can handle any input format and extract
    structured mapping information for SQL generation
    """
    
    def __init__(self, api_key: str, provider: str = "openai"):
        self.api_key = api_key
        self.provider = provider.lower()
        
        # API endpoints
        self.endpoints = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "claude": "https://api.anthropic.com/v1/messages"
        }
    
    async def parse_input(self, raw_input: Any) -> ParsedMapping:
        """
        Main method to parse any input using AI
        
        Args:
            raw_input: Any format input (dict, string, mixed)
        
        Returns:
            ParsedMapping: Normalized structure
        """
        # Convert input to string for AI processing
        input_text = self._prepare_input(raw_input)
        
        # Generate AI prompt
        prompt = self._create_parsing_prompt(input_text)
        
        # Call AI API
        ai_response = await self._call_ai_api(prompt)
        
        # Parse AI response into structured format
        parsed_mapping = self._parse_ai_response(ai_response)
        
        return parsed_mapping
    
    def _prepare_input(self, raw_input: Any) -> str:
        """Convert any input format to string for AI processing"""
        if isinstance(raw_input, str):
            return raw_input
        elif isinstance(raw_input, dict):
            return json.dumps(raw_input, indent=2)
        else:
            return str(raw_input)
    
    def _create_parsing_prompt(self, input_text: str) -> str:
        """Create comprehensive prompt for AI to extract mapping information from Excel content"""
        return f"""
You are a SQL expert analyzing mapping information extracted from an Excel file with multiple sheets.

The Excel file contains vague, unstructured information about how to construct SQL queries. This could include:
- Table names and column mappings
- Join relationships described in natural language
- Business logic and transformation rules
- Output requirements and filters
- Connection details scattered across sheets

Extract and return ONLY a valid JSON object with this exact structure:
{{
    "tables": [
        {{
            "name": "table_name",
            "alias": "optional_alias", 
            "schema": "optional_schema",
            "columns": ["col1", "col2"],
            "description": "what this table represents"
        }}
    ],
    "relationships": [
        {{
            "left_table": "table1",
            "right_table": "table2", 
            "join_type": "INNER|LEFT|RIGHT|FULL",
            "join_condition": "table1.id = table2.table1_id",
            "description": "natural language description from Excel"
        }}
    ],
    "output_columns": [
        {{
            "table": "table_name",
            "column": "column_name",
            "alias": "optional_alias",
            "aggregation": "SUM|COUNT|AVG|etc or null",
            "transformation": "any business logic mentioned"
        }}
    ],
    "filters": [
        {{
            "table": "table_name",
            "column": "column_name", 
            "operator": "=|>|<|LIKE|IN|etc",
            "value": "filter_value",
            "condition": "WHERE|HAVING",
            "description": "business rule from Excel"
        }}
    ],
    "business_logic": [
        {{
            "rule": "description of business rule",
            "implementation": "how to implement in SQL",
            "applies_to": "table or column this affects"
        }}
    ],
    "connection_details": {{
        "server_hostname": "extracted or null",
        "http_path": "extracted or null", 
        "access_token": "extracted or null",
        "database": "default database if mentioned",
        "catalog": "catalog name if mentioned"
    }},
    "metadata": {{
        "description": "what this mapping accomplishes",
        "complexity": "SIMPLE|MEDIUM|COMPLEX",
        "estimated_tables": 0,
        "business_domain": "finance|sales|hr|etc if identifiable",
        "sheets_analyzed": ["list of sheet names that contained useful info"]
    }}
}}

IMPORTANT INSTRUCTIONS:
- Excel content is often vague and incomplete - infer reasonable defaults
- Look for table names that might be references to actual database tables
- Join conditions might be described in business terms - translate to SQL
- Column mappings might be in separate sections - connect them logically
- Some sheets might contain metadata, others actual mappings
- If information is missing, use null or empty arrays but explain in metadata
- Pay attention to sheet names as they often indicate content type
- Business rules might be scattered - consolidate them logically

EXCEL CONTENT TO ANALYZE:
{input_text}

Return only the JSON object, no other text:
"""
    
    async def _call_ai_api(self, prompt: str) -> str:
        """Make HTTP request to AI API"""
        if self.provider == "openai":
            return await self._call_openai(prompt)
        elif self.provider == "claude":
            return await self._call_claude(prompt)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API using raw HTTP request"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "max_tokens": 2000
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.endpoints["openai"], 
                headers=headers, 
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API error: {response.status} - {error_text}")
    
    async def _call_claude(self, prompt: str) -> str:
        """Call Claude API using raw HTTP request"""
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        payload = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 2000,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.endpoints["claude"], 
                headers=headers, 
                json=payload
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["content"][0]["text"]
                else:
                    error_text = await response.text()
                    raise Exception(f"Claude API error: {response.status} - {error_text}")
    
    def _parse_ai_response(self, ai_response: str) -> ParsedMapping:
        """Parse AI response JSON into ParsedMapping object"""
        try:
            # Clean the response and extract JSON
            cleaned_response = ai_response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:-3]
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:-3]
            
            parsed_data = json.loads(cleaned_response)
            
            return ParsedMapping(
                tables=parsed_data.get("tables", []),
                relationships=parsed_data.get("relationships", []),
                output_columns=parsed_data.get("output_columns", []),
                filters=parsed_data.get("filters", []),
                business_logic=parsed_data.get("business_logic", []),
                connection_details=parsed_data.get("connection_details", {}),
                metadata=parsed_data.get("metadata", {})
            )
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse AI response as JSON: {e}")
        except Exception as e:
            raise Exception(f"Error processing AI response: {e}")


# Async context manager for cleaner usage
class AIParser:
    def __init__(self, api_key: str, provider: str = "openai"):
        self.parser = AIInputParser(api_key, provider)
    
    async def __aenter__(self):
        return self.parser
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
