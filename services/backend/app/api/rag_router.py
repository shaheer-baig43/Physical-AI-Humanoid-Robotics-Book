from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import logging

from app.services.rag_service import rag_service # Updated import path
from app.core.db import log_conversation # Updated import path

router = APIRouter()
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    selected_text: Optional[str] = None
    user_id: Optional[str] = None # Added user_id

class ChatResponse(BaseModel):
    answer: str
    session_id: str

@router.post("/v1/rag", response_model=ChatResponse, tags=["RAG"]) # Changed endpoint path and tag
async def rag_query(request: ChatRequest): # Renamed function for clarity
    """
    Main RAG endpoint to query the chatbot.
    Receives a query, optional selected text, and optional user_id; returns an answer.
    """
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        answer = rag_service.answer_query(
            query=request.query, 
            selected_text=request.selected_text, 
            user_id=request.user_id # Pass user_id
        )
        
        # Log the conversation to the database
        log_conversation(
            session_id=session_id,
            user_message=request.query,
            bot_response=answer,
            selected_text=request.selected_text,
            user_id=request.user_id # Pass user_id to log
        )
        
        return ChatResponse(answer=answer, session_id=session_id)
        
    except Exception as e:
        logger.error(f"Error during RAG processing for session {session_id}, user {request.user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An internal error occurred: {e}")
