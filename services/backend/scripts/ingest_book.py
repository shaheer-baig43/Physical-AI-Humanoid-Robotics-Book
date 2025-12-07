import os
import sys
import glob
import re
from typing import List, Dict, Any
import uuid # Needed for doc_id
import logging # Added for logging
logging.basicConfig(level=logging.INFO) # Configure basic logging

# Calculate the project root directory (e.g., my-website/)
# __file__ is ingest_book.py
# os.path.dirname(__file__) is services/backend/scripts/
# '..' one level up is services/backend/
# '..' two levels up is services/
# '..' three levels up is my-website/ (the project root)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
print(f"Calculated PROJECT_ROOT: {PROJECT_ROOT}")
sys.path.insert(0, PROJECT_ROOT) # Insert at the beginning of sys.path

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings # Switched to GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore # Updated: Use QdrantVectorStore
from qdrant_client import QdrantClient, models

# The import paths are now relative to PROJECT_ROOT
from services.backend.app.core.config import settings
from services.backend.app.core.db import save_document_metadata
