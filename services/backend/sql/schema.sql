-- SQL Schema for Neon Postgres Database

-- Table: users
-- Stores user profile data collected during signup, linked to Better-Auth user ID.
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    better_auth_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    programming_skill_level VARCHAR(50), -- e.g., 'beginner', 'intermediate', 'advanced'
    robotics_experience VARCHAR(50),    -- e.g., 'none', 'basic', 'intermediate', 'advanced'
    hardware_access TEXT,               -- Comma-separated values, e.g., 'Arduino,GPU'
    preferred_language VARCHAR(10),     -- e.g., 'en', 'ur'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index on better_auth_id for quick lookups
CREATE INDEX IF NOT EXISTS idx_users_better_auth_id ON users(better_auth_id);


-- Table: personalization_cache
-- Caches personalized chapter content to avoid re-generating for the same user/chapter.
CREATE TABLE IF NOT EXISTS personalization_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_path VARCHAR(512) NOT NULL, -- Path to the original markdown file
    original_markdown_hash VARCHAR(64) NOT NULL, -- SHA256 hash of original markdown content
    personalized_markdown TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE (user_id, chapter_path, original_markdown_hash) -- Ensure unique cache entry per user, chapter, and content version
);

-- Index for quick lookups by user and chapter
CREATE INDEX IF NOT EXISTS idx_personalization_cache_user_chapter ON personalization_cache(user_id, chapter_path);


-- Table: translation_cache
-- Caches translated chapter content.
CREATE TABLE IF NOT EXISTS translation_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_path VARCHAR(512) NOT NULL, -- Path to the original markdown file
    target_language VARCHAR(10) NOT NULL, -- e.g., 'ur' for Urdu
    original_markdown_hash VARCHAR(64) NOT NULL, -- SHA256 hash of original markdown content
    translated_markdown TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (chapter_path, target_language, original_markdown_hash) -- Ensure unique cache entry per chapter, language, and content version
);

-- Index for quick lookups by chapter and language
CREATE INDEX IF NOT EXISTS idx_translation_cache_chapter_language ON translation_cache(chapter_path, target_language);


-- Table: document_metadata
-- Stores metadata for documents ingested into Qdrant, mirroring the vector DB.
CREATE TABLE IF NOT EXISTS document_metadata (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doc_id VARCHAR(255) UNIQUE NOT NULL, -- Unique ID for the document in Qdrant (or generated)
    file_path VARCHAR(512) UNIQUE NOT NULL, -- Original path of the markdown file
    title VARCHAR(255),
    summary TEXT, -- Optional: LLM-generated summary during ingestion
    qdrant_vector_ids TEXT[], -- Array of Qdrant point IDs associated with this document
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for quick lookups by file_path
CREATE INDEX IF NOT EXISTS idx_document_metadata_file_path ON document_metadata(file_path);
