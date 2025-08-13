"""
SSE (Server-Sent Events) utilities for streaming responses
"""
from typing import AsyncGenerator, Dict, Any


async def create_sse_event(event_type: str, data: str) -> Dict[str, str]:
    """
    Create a properly formatted SSE event
    
    Args:
        event_type: Type of the event (status, data, error, etc.)
        data: Event data as string
    
    Returns:
        Dictionary with event and data keys
    """
    return {"event": event_type, "data": data}


async def stream_status_event(message: str) -> Dict[str, str]:
    """Helper to create status events"""
    return await create_sse_event("status", message)


async def stream_error_event(error_message: str) -> Dict[str, str]:
    """Helper to create error events"""
    return await create_sse_event("error", error_message)


async def stream_data_event(data: str) -> Dict[str, str]:
    """Helper to create data events"""
    return await create_sse_event("data", data)


async def stream_close_event(message: str) -> Dict[str, str]:
    """Helper to create close events"""
    return await create_sse_event("close", message)
