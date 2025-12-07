# Physical AI & Humanoid Robotics Course Platform

This project implements a full-stack platform for an educational course on Physical AI and Humanoid Robotics. It features a Docusaurus-based frontend for course content and a FastAPI backend for AI-powered functionalities, including a RAG chatbot, chapter personalization, and Urdu translation, all integrated with user authentication and profiling.

## Table of Contents

1.  [Project Structure](#project-structure)
2.  [Features](#features)
3.  [Setup Guide](#setup-guide)
    *   [Prerequisites](#prerequisites)
    *   [Environment Variables](#environment-variables)
    *   [Database Setup (Neon Postgres)](#database-setup-neon-postgres)
    *   [Qdrant Cloud Setup](#qdrant-cloud-setup)
    *   [Better-Auth Setup](#better-auth-setup)
    *   [Python Backend Setup](#python-backend-setup)
    *   [Frontend (Docusaurus) Setup](#frontend-docusaurus-setup)
4.  [Running the Application](#running-the-application)
    *   [Ingest Course Content](#ingest-course-content)
    *   [Start Backend Server](#start-backend-server)
    *   [Start Frontend Server](#start-frontend-server)
5.  [API Routes](#api-routes)
6.  [Frontend Components](#frontend-components)
7.  [SQL Schemas](#sql-schemas)
8.  [Subagent YAML Files](#subagent-yaml-files)
9.  [Bonus Scoring Safety Considerations](#bonus-scoring-safety-considerations)

---

## 1. Project Structure

```
.
├── services/
│   ├── backend/
│   │   ├── app/                      # FastAPI Application
│   │   │   ├── api/                  # API Routers (auth, rag, personalization, translation)
│   │   │   ├── core/                 # Core utilities (config, db, agents)
│   │   │   ├── services/             # Business Logic (e.g., RAGService)
│   │   │   └── main.py               # Main FastAPI app entry point
│   │   ├── scripts/                  # Backend scripts (e.g., ingestion)
│   │   │   └── ingest_book.py
│   │   ├── subagents/                # Claude Subagent Definitions
│   │   │   └── agents/               # YAML files for each subagent
│   │   ├── sql/                      # SQL schema definitions
│   │   │   └── schema.sql
│   │   └── .env.example              # Example environment variables for backend
│   └── frontend/
│       └── docs/                     # Docusaurus Markdown content (course chapters)
├── src/                              # Docusaurus Frontend Source
│   ├── components/                   # React Components (RAG Chat, Buttons, Auth forms)
│   │   ├── RAGChatWidget/
│   │   │   ├── index.jsx
│   │   │   └── styles.module.css
│   │   ├── PersonalizeChapterButton.jsx
│   │   ├── TranslateUrduButton.jsx
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   └── ChapterButtons.module.css # Shared styles
│   ├── pages/                        # Docusaurus Custom Pages (login, signup)
│   │   ├── login.jsx
│   │   └── signup.jsx
│   ├── theme/                        # Swizzled Docusaurus Theme Components
│   │   ├── DocItem/
│   │   │   └── index.tsx             # Modified for personalization/translation buttons
│   │   └── Layout/
│   │       └── index.tsx             # Modified for RAG chat widget and auth status
│   └── apiClient.js                  # Shared JavaScript API client for frontend
├── docusaurus.config.ts              # Docusaurus configuration
├── sidebars.ts                       # Docusaurus sidebar configuration
├── package.json                      # Frontend dependencies
├── package-lock.json
└── tsconfig.json
```

## 2. Features

This platform integrates several advanced features:

*   **RAG Chatbot:** A Retrieval-Augmented Generation chatbot allowing book-wide Q&A and selected-text-only questions.
*   **User Authentication & Profiling:** Secure signup/signin via Better-Auth, with user profiling data stored in Neon Postgres.
*   **Chapter Personalization:** Dynamically rewrites chapter content based on user's skill level, experience, and hardware access, using a Claude `personalization_agent`.
*   **Urdu Translation:** Translates chapter content to academic Urdu on demand, preserving technical terms and code, using a Claude `urdu_translator` agent.
*   **Ingestion Pipeline:** Robustly processes markdown documents, removes frontmatter, chunks text, generates embeddings, and mirrors metadata to Neon Postgres.
*   **Caching:** Caches personalized and translated content in Neon Postgres to reduce redundant LLM calls.
*   **Claude Subagents:** Modular AI agents defined in YAML for various tasks (robotics expert, simplifier, translator, personalizer, ingestion).

## 3. Setup Guide

### Prerequisites

*   **Python 3.9+** and `pip`
*   **Node.js 18+** and `npm`
*   **Git**
*   **Better-Auth Account:** For user authentication.
*   **Neon.tech Account:** For PostgreSQL database.
*   **Qdrant Cloud Account:** For vector database.
*   **Google AI Studio Account:** For Gemini API Key (for LLM and embeddings).

### Environment Variables

Create a file named `.env` in the `services/backend/` directory. Copy the contents of `services/backend/.env.example` into it and fill in your actual credentials:

```
# Gemini
GEMINI_API_KEY="your_gemini_api_key"

# Qdrant
QDRANT_CLOUD_URL="your_qdrant_cloud_url"
QDRANT_API_KEY="your_qdrant_api_key"

# Neon
NEON_DATABASE_URL="your_neon_database_url"

# Better-Auth (OAuth2/OpenID Connect)
BETTER_AUTH_CLIENT_ID="your_better_auth_client_id"
BETTER_AUTH_CLIENT_SECRET="your_better_auth_client_secret"
BETTER_AUTH_AUTHORIZATION_URL="https://auth.better-auth.com/oauth/authorize" # Replace with actual URL from Better-Auth
BETTER_AUTH_TOKEN_URL="https://auth.better-auth.com/oauth/token"             # Replace with actual URL
BETTER_AUTH_USERINFO_URL="https://auth.better-auth.com/oauth/userinfo"       # Replace with actual URL
BETTER_AUTH_REDIRECT_URI="http://localhost:8000/api/v1/auth/callback"        # This MUST match the redirect URI configured in Better-Auth
BETTER_AUTH_SCOPE="openid email profile"

# Security
SECRET_KEY="a_very_long_and_random_secret_key_for_jwt_signing" # GENERATE A STRONG, RANDOM KEY!
HTTPS_ENABLED="False" # Set to "True" if deploying with HTTPS
```

**How to generate API keys/credentials:**

*   **Gemini API Key:** Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
*   **Qdrant Cloud URL & API Key:** Create a cluster at [Qdrant Cloud](https://cloud.qdrant.io/). Find credentials in your cluster's overview.
*   **Neon Database URL:** Create a project at [Neon.tech](https://neon.tech/). Find the connection string in your project dashboard.
*   **Better-Auth Credentials:** Register your application with [Better-Auth](https://www.better-auth.com/) to obtain `CLIENT_ID`, `CLIENT_SECRET`, and configure `REDIRECT_URI`. Obtain the Authorization, Token, and UserInfo URLs from their documentation.

### Database Setup (Neon Postgres)

The FastAPI backend will automatically create the necessary tables (`users`, `chat_logs`, `personalization_cache`, `translation_cache`, `document_metadata`) when it starts if they don't exist. Ensure your `NEON_DATABASE_URL` is correct.

You can also run the SQL directly from `services/backend/sql/schema.sql` using a PostgreSQL client if you prefer manual setup or want to inspect the schema.

### Qdrant Cloud Setup

The `ingest_book.py` script will create the Qdrant collection (`physical_ai_book_gemini`) if it doesn't exist. Ensure `QDRANT_CLOUD_URL` and `QDRANT_API_KEY` are correct.

### Better-Auth Setup

1.  **Register your application** with Better-Auth.
2.  **Configure Redirect URI:** Set the Redirect URI in your Better-Auth application settings to `http://localhost:8000/api/v1/auth/callback`. This is critical.
3.  **Obtain Credentials:** Get your Client ID, Client Secret, and the Authorization, Token, and UserInfo endpoints from Better-Auth's dashboard/documentation.

### Python Backend Setup

Navigate to the `services/backend/` directory and install dependencies:

```bash
cd services/backend
pip install -r requirements.txt
cd ../.. # Go back to project root
```

### Frontend (Docusaurus) Setup

Navigate to the project root and install Docusaurus dependencies:

```bash
npm install
```

## 4. Running the Application

### Ingest Course Content

This step populates your Qdrant vector database and Neon Postgres `document_metadata` table. You **must** run this successfully once. If you change documentation content, re-run this script.

From the project root:

```bash
python services/backend/scripts/ingest_book.py
```
Monitor the output for `Ingestion process completed successfully!`.

### Start Backend Server

Open a **new terminal** at the project root and run:

```bash
uvicorn services.backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
The `--reload` flag is useful for development as it restarts the server on code changes.

### Start Frontend Server

Open **another new terminal** at the project root and run:

```bash
npm start
```

Your Docusaurus site will open in your browser, typically at `http://localhost:3000`.

## 5. API Routes

All API routes are exposed by the FastAPI backend (running on `http://localhost:8000`).

*   **`GET /health`**: Health check.
*   **Authentication (Better-Auth):**
    *   `GET /api/v1/auth/login`
    *   `GET /api/v1/auth/callback`
    *   `GET /api/v1/auth/me`
    *   `POST /api/v1/auth/logout`
*   **User Profile:**
    *   `POST /api/v1/user/profile` (Requires authentication)
*   **RAG Chatbot:**
    *   `POST /api/v1/rag` (Input: `{"query": "...", "selected_text": "optional", "user_id": "optional"}`)
*   **Chapter Personalization:**
    *   `POST /api/v1/personalize` (Input: `{"chapter_markdown": "...", "chapter_path": "..."}`, Requires authentication)
*   **Urdu Translation:**
    *   `POST /api/v1/translate?lang=ur` (Input: `{"chapter_markdown": "...", "chapter_path": "..."}`)

## 6. Frontend Components

*   **`src/components/RAGChatWidget/index.jsx`**: Anchored bottom-right, supports book-wide and selected-text QA.
*   **`src/components/PersonalizeChapterButton.jsx`**: Button for personalizing chapter content.
*   **`src/components/TranslateUrduButton.jsx`**: Button for translating chapter content to Urdu.
*   **`src/components/Login.jsx`**: Login form, redirects to Better-Auth.
*   **`src/components/Signup.jsx`**: User profile completion form after Better-Auth login.
*   **`src/apiClient.js`**: Shared client for all backend API interactions.
*   **`src/theme/Layout/index.tsx`**: Displays login/signup status and `RAGChatWidget`.
*   **`src/theme/DocItem/index.tsx`**: Injects `PersonalizeChapterButton` and `TranslateUrduButton` into chapter pages.

## 7. SQL Schemas

The following tables are created in Neon Postgres. See `services/backend/sql/schema.sql` for full definitions.

*   `users`: Stores user authentication (Better-Auth ID) and profiling data.
*   `personalization_cache`: Caches personalized chapter content.
*   `translation_cache`: Caches translated chapter content.
*   `document_metadata`: Mirrors metadata of documents ingested into Qdrant.
*   `chat_logs`: Stores chat history for the RAG chatbot.

## 8. Subagent YAML Files

Located in `services/backend/subagents/agents/`. Each defines an AI subagent with `id`, `display_name`, `description`, `system_prompt`, `input_schema`, `output_schema`, and `example_invocation`.

*   `robotic_expert.yaml`
*   `beginner_simplifier.yaml`
*   `urdu_translator.yaml`
*   `personalization_agent.yaml`
*   `ingestion_agent.yaml`

## 9. Bonus Scoring Safety Considerations

*   **All AI prompts must be reusable:** Achieved via YAML-defined subagents and `AgentManager`.
*   **All subagents must be stored as YAML:** Achieved.
*   **All features must be toggleable:** Currently, features are enabled by default through router inclusion. For production, a more robust toggle system would involve environment variables (`settings.FEATURE_ENABLE_X`) checked in FastAPI routers or frontend components.
*   **All user-generated AI content must be cached:** Achieved for personalization and translation via dedicated Neon Postgres cache tables.
*   **No hardcoded content:** API keys and sensitive configurations are managed via `.env` files. Agent prompts are in external YAML.
*   **Production-grade code:** Structured with FastAPI, Pydantic, LangChain, clear separation of concerns, and logging. Error handling is present.

---
**Note:** This setup assumes a development environment. For production deployment, considerations like HTTPS for the backend, more robust session management, detailed logging, and proper error monitoring would be required.