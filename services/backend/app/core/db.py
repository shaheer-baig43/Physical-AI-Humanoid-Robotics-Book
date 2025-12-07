import psycopg2
from app.core.config import settings # Updated import path
import logging
from typing import Optional, List, Dict, Any
import json
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """Establishes a connection to the Neon database."""
    try:
        conn = psycopg2.connect(settings.NEON_DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Could not connect to the database: {e}")
        return None

def create_users_table():
    """Creates the users table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    google_id VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    programming_skill_level VARCHAR(50), -- e.g., 'beginner', 'intermediate', 'advanced'
                    robotics_experience VARCHAR(50),    -- e.g., 'none', 'basic', 'intermediate', 'advanced'
                    hardware_access TEXT,               -- Comma-separated values, e.g., 'Arduino,GPU'
                    preferred_language VARCHAR(10),     -- e.g., 'en', 'ur'
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
            """)
            conn.commit()
            logger.info("'users' table checked/created successfully.")
    except psycopg2.Error as e:
        logger.error(f"Error creating users table: {e}")
    finally:
        if conn:
            conn.close()


def get_user_profile_by_google_id(google_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a user's profile from the database using their Google ID."""
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, programming_skill_level, robotics_experience, hardware_access, preferred_language, email
                FROM users
                WHERE google_id = %s;
            """, (google_id,))
            result = cur.fetchone()
            if result:
                return {
                    "id": result[0],
                    "programming_skill_level": result[1],
                    "robotics_experience": result[2],
                    "hardware_access": result[3],
                    "preferred_language": result[4],
                    "email": result[5],
                }
            return None
    except psycopg2.Error as e:
        logger.error(f"Error retrieving user profile for google_id {google_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()


def create_chat_logs_table():
    """Creates the chat_logs table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS chat_logs (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    user_id UUID REFERENCES users(id) ON DELETE SET NULL, -- Added user_id
                    user_message TEXT NOT NULL,
                    bot_response TEXT NOT NULL,
                    selected_text TEXT,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                );
            """)
            conn.commit()
            logger.info("'chat_logs' table checked/created successfully.")
    except psycopg2.Error as e:
        logger.error(f"Error creating chat_logs table: {e}")
    finally:
        if conn:
            conn.close()

def create_document_metadata_table():
    """Creates the document_metadata table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS document_metadata (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    doc_id VARCHAR(255) UNIQUE NOT NULL, -- Unique ID for the document (e.g., hash or Qdrant ID if single per doc)
                    file_path VARCHAR(512) UNIQUE NOT NULL, -- Original path of the markdown file
                    title VARCHAR(255),
                    summary TEXT, -- Optional: LLM-generated summary during ingestion
                    qdrant_vector_ids TEXT[], -- Array of Qdrant point IDs associated with this document
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_document_metadata_file_path ON document_metadata(file_path);
            """)
            conn.commit()
            logger.info("'document_metadata' table checked/created successfully.")
    except psycopg2.Error as e:
        logger.error(f"Error creating document_metadata table: {e}")
    finally:
        if conn:
            conn.close()

def create_personalization_cache_table():
    """Creates the personalization_cache table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS personalization_cache (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    chapter_path VARCHAR(512) NOT NULL,
                    original_markdown_hash VARCHAR(64) NOT NULL,
                    personalized_markdown TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (user_id, chapter_path, original_markdown_hash)
                );
                CREATE INDEX IF NOT EXISTS idx_personalization_cache_user_chapter ON personalization_cache(user_id, chapter_path);
            """)
            conn.commit()
            logger.info("'personalization_cache' table checked/created successfully.")
    except psycopg2.Error as e:
        logger.error(f"Error creating personalization_cache table: {e}")
    finally:
        if conn:
            conn.close()

def create_translation_cache_table():
    """Creates the translation_cache table if it doesn't exist."""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS translation_cache (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    chapter_path VARCHAR(512) NOT NULL,
                    target_language VARCHAR(10) NOT NULL,
                    original_markdown_hash VARCHAR(64) NOT NULL,
                    translated_markdown TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE (chapter_path, target_language, original_markdown_hash)
                );
                CREATE INDEX IF NOT EXISTS idx_translation_cache_chapter_language ON translation_cache(chapter_path, target_language);
            """)
            conn.commit()
            logger.info("'translation_cache' table checked/created successfully.")
    except psycopg2.Error as e:
        logger.error(f"Error creating translation_cache table: {e}")
    finally:
        if conn:
            conn.close()

# Combined initialization function
def initialize_database_tables():
    create_users_table()
    create_chat_logs_table()
    create_document_metadata_table()
    create_personalization_cache_table()
    create_translation_cache_table()

def log_conversation(session_id: str, user_message: str, bot_response: str, selected_text: Optional[str] = None, user_id: Optional[str] = None):
    """Logs a user message and the bot's response to the database."""
    conn = get_db_connection()
    if conn is None:
        logger.error("Skipping conversation log due to no DB connection.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO chat_logs (session_id, user_id, user_message, bot_response, selected_text)
                VALUES (%s, %s, %s, %s, %s);
            """, (session_id, user_id, user_message, bot_response, selected_text))
            conn.commit()
            logger.info(f"Logged conversation for session: {session_id}, user: {user_id}")
    except psycopg2.Error as e:
        logger.error(f"Error logging conversation: {e}")
    finally:
        if conn:
            conn.close()

def save_document_metadata(doc_id: str, file_path: str, title: str, summary: Optional[str], qdrant_vector_ids: List[str]):
    """Saves document metadata to the database."""
    conn = get_db_connection()
    if conn is None:
        logger.error("Skipping document metadata save due to no DB connection.")
        return

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO document_metadata (doc_id, file_path, title, summary, qdrant_vector_ids)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (file_path) DO UPDATE SET
                    doc_id = EXCLUDED.doc_id,
                    title = EXCLUDED.title,
                    summary = EXCLUDED.summary,
                    qdrant_vector_ids = EXCLUDED.qdrant_vector_ids,
                    updated_at = CURRENT_TIMESTAMP;
            """, (doc_id, file_path, title, summary, qdrant_vector_ids))
            conn.commit()
            logger.info(f"Saved/Updated metadata for document: {file_path}")
    except psycopg2.Error as e:
        logger.error(f"Error saving document metadata: {e}")
    finally:
        if conn:
            conn.close()

def upsert_user_profile(
    google_id: str,
    email: str,
    programming_skill_level: Optional[str] = None,
    robotics_experience: Optional[str] = None,
    hardware_access: Optional[str] = None,
    preferred_language: Optional[str] = None,
) -> Optional[uuid.UUID]:
    """
    Inserts a new user profile or updates an existing one based on google_id.
    Returns the user's UUID.
    """
    conn = get_db_connection()
    if conn is None:
        logger.error("Skipping user profile upsert due to no DB connection.")
        return None

    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (google_id, email, programming_skill_level, robotics_experience, hardware_access, preferred_language)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (google_id) DO UPDATE SET
                    email = EXCLUDED.email,
                    programming_skill_level = COALESCE(EXCLUDED.programming_skill_level, users.programming_skill_level),
                    robotics_experience = COALESCE(EXCLUDED.robotics_experience, users.robotics_experience),
                    hardware_access = COALESCE(EXCLUDED.hardware_access, users.hardware_access),
                    preferred_language = COALESCE(EXCLUDED.preferred_language, users.preferred_language),
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id;
            """, (google_id, email, programming_skill_level, robotics_experience, hardware_access, preferred_language))
            user_id = cur.fetchone()[0]
            conn.commit()
            logger.info(f"Upserted user profile for google_id: {google_id}, user_id: {user_id}")
            return user_id
    except psycopg2.Error as e:
        logger.error(f"Error upserting user profile for google_id {google_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()



def get_user_profile(user_id: uuid.UUID) -> Optional[Dict[str, Any]]:
    """Retrieves a user's profile from the database."""
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT programming_skill_level, robotics_experience, hardware_access, preferred_language
                FROM users
                WHERE id = %s;
            """, (user_id,))
            result = cur.fetchone()
            if result:
                return {
                    "programming_skill_level": result[0],
                    "robotics_experience": result[1],
                    "hardware_access": result[2],
                    "preferred_language": result[3],
                }
            return None
    except psycopg2.Error as e:
        logger.error(f"Error retrieving user profile for {user_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def save_personalization_cache(user_id: uuid.UUID, chapter_path: str, original_markdown_hash: str, personalized_markdown: str):
    """Saves personalized chapter content to the cache."""
    conn = get_db_connection()
    if conn is None:
        logger.error("Skipping personalization cache save due to no DB connection.")
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO personalization_cache (user_id, chapter_path, original_markdown_hash, personalized_markdown)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id, chapter_path, original_markdown_hash) DO UPDATE SET
                    personalized_markdown = EXCLUDED.personalized_markdown,
                    created_at = CURRENT_TIMESTAMP;
            """, (user_id, chapter_path, original_markdown_hash, personalized_markdown))
            conn.commit()
            logger.info(f"Saved/Updated personalization cache for user {user_id}, chapter {chapter_path}")
    except psycopg2.Error as e:
        logger.error(f"Error saving personalization cache: {e}")
    finally:
        if conn:
            conn.close()

def save_translation_cache(chapter_path: str, target_language: str, original_markdown_hash: str, translated_markdown: str):
    """Saves translated chapter content to the cache."""
    conn = get_db_connection()
    if conn is None:
        logger.error("Skipping translation cache save due to no DB connection.")
        return
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO translation_cache (chapter_path, target_language, original_markdown_hash, translated_markdown)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (chapter_path, target_language, original_markdown_hash) DO UPDATE SET
                    translated_markdown = EXCLUDED.translated_markdown,
                    created_at = CURRENT_TIMESTAMP;
            """, (chapter_path, target_language, original_markdown_hash, translated_markdown))
            conn.commit()
            logger.info(f"Saved/Updated translation cache for chapter {chapter_path}, language {target_language}")
    except psycopg2.Error as e:
        logger.error(f"Error saving translation cache: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # This allows running the script directly to initialize all database tables
    print("Initializing database tables...")
    initialize_database_tables()
    print("Database initialization complete.")