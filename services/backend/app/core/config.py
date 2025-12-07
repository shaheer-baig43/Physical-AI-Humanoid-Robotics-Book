import os
from dotenv import load_dotenv

# Load environment variables from .env file at the root of services/backend
load_dotenv(dotenv_path='.env') # Updated path

class Settings:
    # OpenAI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    GEMINI_EMBEDDING_MODEL: str = "models/text-embedding-004"
    GEMINI_CHAT_MODEL: str = "gemini-1.5-flash-latest"

    # Qdrant
    QDRANT_CLOUD_URL: str = os.getenv("QDRANT_CLOUD_URL")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION_NAME: str = "physical_ai_book_gemini" # Changed for Gemini

    # Neon
    NEON_DATABASE_URL: str = os.getenv("NEON_DATABASE_URL")

    # Ingestion
    DOCS_DIRECTORY: str = "services/frontend/docs"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    # The embedding dimension for OpenAI's text-embedding-ada-002 model
    VECTOR_SIZE: int = 768 
    
        # Security
    
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    
    HTTPS_ENABLED: bool = os.getenv("HTTPS_ENABLED", "False").lower() == "true"
    
    
    
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI")

settings = Settings()

# Basic validation
if not all([
    settings.GEMINI_API_KEY, 
    settings.QDRANT_CLOUD_URL, 
    settings.QDRANT_API_KEY, 
    settings.NEON_DATABASE_URL,
    settings.GOOGLE_CLIENT_ID,
    settings.GOOGLE_CLIENT_SECRET,
    settings.GOOGLE_REDIRECT_URI,
    settings.SECRET_KEY, 
]):
    raise ValueError("One or more essential environment variables are missing. Please check your .env file.")
