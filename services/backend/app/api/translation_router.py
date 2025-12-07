from fastapi import APIRouter, Query, Depends # Added APIRouter, Query, and Depends
from langchain_google_genai import ChatGoogleGenerativeAI # Switched to ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import uuid
import logging
import hashlib # For markdown hash

from app.core.config import settings
from app.core.db import save_translation_cache # Need this DB function
from app.core.agents import AgentManager
from app.api.auth_router import get_current_user # To get logged-in user (though translation might not strictly require auth)

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Request Models ---
class TranslationRequest(BaseModel):
    chapter_markdown: str
    chapter_path: str # Identifier for the chapter, e.g., "docs/module-1/intro.md"

# --- Response Models ---
class TranslationResponse(BaseModel):
    translated_markdown: str
    cached: bool = False

# --- Agent Interaction (Assuming LLM client is available globally or passed) ---
# This would typically be a dependency injection or a global instance from main.py
# For now, we'll instantiate a ChatGoogleGenerativeAI for the agents
agent_llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_CHAT_MODEL,
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.3, # Translation usually needs lower temperature for accuracy
    convert_system_message_to_human=True, # For Gemini
)

@router.post("/v1/translate", response_model=TranslationResponse, tags=["Translation"])
async def translate_chapter(
    request: TranslationRequest,
    lang: str = Query(..., description="Target language code (e.g., 'ur' for Urdu)"),
    current_user: Optional[Dict] = Depends(get_current_user) # Authentication optional for translation
):
    """
    Translates a chapter's markdown content to the specified target language.
    Calls the Claude urdu_translator agent (or other relevant agent based on lang).
    """
    if lang != "ur":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Urdu translation ('ur') is currently supported.")

    # Generate a hash for the original markdown to use as cache key
    original_markdown_hash = hashlib.sha256(request.chapter_markdown.encode('utf-8')).hexdigest()

    # 1. Check cache first (implementation not shown here, assumed to be part of save_translation_cache or a separate get)
    # For now, we'll always call the agent and save/update cache
    
    # 2. Call Claude urdu_translator agent
    try:
        agent_inputs = {
            "english_text": request.chapter_markdown,
        }
        
        agent_output = AgentManager.run_agent(
            agent_id="urdu_translator",
            inputs=agent_inputs,
            llm_client=agent_llm # Pass the instantiated LLM client
        )
        
        translated_markdown = agent_output.get("urdu_text")
        if not translated_markdown:
            raise ValueError("Urdu translator agent did not return urdu_text.")

        # 3. Cache translations
        save_translation_cache(
            chapter_path=request.chapter_path,
            target_language=lang,
            original_markdown_hash=original_markdown_hash,
            translated_markdown=translated_markdown
        )
        
        return TranslationResponse(translated_markdown=translated_markdown, cached=False)
    
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Error during chapter translation to {lang} for chapter {request.chapter_path}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to translate chapter content.")

