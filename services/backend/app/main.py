from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.api import rag_router
from app.api import auth_router
from app.api import personalization_router
from app.api import translation_router # New import for translation_router
from app.core.db import initialize_database_tables # Updated for all tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    print("Application startup...")
    # Initialize all database tables
    initialize_database_tables() # Use the combined initialization function
    yield
    # On shutdown
    print("Application shutdown.")

app = FastAPI(
    title="Physical AI Course Chatbot",
    description="A chatbot for the Physical AI & Humanoid Robotics course.",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows the Docusaurus dev server
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to ensure the service is running.
    """
    return {"status": "ok"}

# Include the RAG router
app.include_router(rag_router.router, prefix="/api")
# Include the Auth router
app.include_router(auth_router.router, prefix="/api")
# Include the Personalization router
app.include_router(personalization_router.router, prefix="/api")
# Include the Translation router
app.include_router(translation_router.router, prefix="/api") # New router inclusion

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
