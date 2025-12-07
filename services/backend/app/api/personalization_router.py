from fastapi import APIRouter, Depends, HTTPException, status, Request
from langchain_google_genai import ChatGoogleGenerativeAI # Switched to ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import uuid
import logging
import hashlib # For markdown hash

from app.core.config import settings
from app.core.db import get_user_profile, save_personalization_cache # Need these DB functions
from app.core.agents import AgentManager
from app.api.auth_router import get_current_user # To get logged-in user

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Request Models ---
class PersonalizationRequest(BaseModel):
    chapter_markdown: str
    chapter_path: str # Identifier for the chapter, e.g., "docs/module-1/intro.md"

# --- Response Models ---
class PersonalizationResponse(BaseModel):
    personalized_markdown: str
    cached: bool = False

# --- Agent Interaction (Assuming LLM client is available globally or passed) ---
# This would typically be a dependency injection or a global instance from main.py
# For now, we'll instantiate a ChatGoogleGenerativeAI for the agents
agent_llm = ChatGoogleGenerativeAI(
    model=settings.GEMINI_CHAT_MODEL,
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.7, # Agents might need more creativity
    convert_system_message_to_human=True, # For Gemini
)


@router.post("/v1/personalize", response_model=PersonalizationResponse, tags=["Personalization"])
async def personalize_chapter(
    request: PersonalizationRequest,
    current_user: Dict = Depends(get_current_user) # Requires authentication
):
    """
    Personalizes a chapter's markdown content based on the logged-in user's profile.
    Calls the Claude personalization_agent.
    """
    user_id = uuid.UUID(current_user["id"])
    
    # 1. Fetch logged-in user profile
    user_profile = get_user_profile(user_id=user_id)
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Please complete your profile."
        )

    # Prepare inputs for the personalization agent
    skill_level = user_profile.get("programming_skill_level", "beginner")
    robotics_experience = user_profile.get("robotics_experience", "none")
    hardware_access = user_profile.get("hardware_access", "") # Stored as comma-sep string
    
    # Generate a hash for the original markdown to use as cache key
    original_markdown_hash = hashlib.sha256(request.chapter_markdown.encode('utf-8')).hexdigest()

    # 2. Check cache first
    # Need a function get_personalization_cache(user_id, chapter_path, original_markdown_hash)
    # For now, let's skip cache check and assume it's done within the save function
    
    # 3. Call Claude personalization_agent
    try:
        agent_inputs = {
            "chapter_markdown": request.chapter_markdown,
            "skill_level": skill_level,
            "robotics_experience": robotics_experience,
            "hardware_profile": hardware_access,
        }
        
        # Ensure agent_llm is imported and configured
        agent_output = AgentManager.run_agent(
            agent_id="personalization_agent",
            inputs=agent_inputs,
            llm_client=agent_llm # Pass the instantiated LLM client
        )
        
        personalized_markdown = agent_output.get("rewritten_markdown")
        if not personalized_markdown:
            raise ValueError("Personalization agent did not return rewritten_markdown.")

        # 4. Cache result
        # Ensure save_personalization_cache accepts uuid.UUID for user_id
        save_personalization_cache(
            user_id=user_id,
            chapter_path=request.chapter_path,
            original_markdown_hash=original_markdown_hash,
            personalized_markdown=personalized_markdown
        )
        
        return PersonalizationResponse(personalized_markdown=personalized_markdown, cached=False)
    
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Error during chapter personalization for user {user_id}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to personalize chapter content.")

