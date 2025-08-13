"""
Database utilities for Databricks SQL operations
"""
from databricks import sql
import asyncio
from typing import Tuple, List, Dict, Any


async def execute_sql_async(
    sql_query: str,
    server_hostname: str,
    http_path: str,
    access_token: str,
    timeout: int = 30
) -> Tuple[List[str], List[Tuple]]:
    """
    Execute SQL query asynchronously against Databricks
    
    Args:
        sql_query: SQL query to execute
        server_hostname: Databricks server hostname
        http_path: Databricks HTTP path
        access_token: Databricks access token
        timeout: Query timeout in seconds
    
    Returns:
        Tuple of (column_names, rows)
    
    Raises:
        asyncio.TimeoutError: If query times out
        Exception: For other SQL execution errors
    """
    def run_sql_sync():
        with sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return columns, rows
    
    return await asyncio.wait_for(
        asyncio.get_event_loop().run_in_executor(None, run_sql_sync),
        timeout=timeout
    )


def validate_connection_params(
    sql_query: str,
    server_hostname: str,
    http_path: str,
    access_token: str
) -> bool:
    """
    Validate that all required connection parameters are provided
    
    Returns:
        True if all parameters are provided, False otherwise
    """
    return all([sql_query, server_hostname, http_path, access_token])


def format_row_data(columns: List[str], row: Tuple) -> Dict[str, Any]:
    """
    Convert a row tuple to a dictionary using column names
    
    Args:
        columns: List of column names
        row: Row data tuple
    
    Returns:
        Dictionary with column names as keys
    """
    return dict(zip(columns, row))
