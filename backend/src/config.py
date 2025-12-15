"""
Configuration settings for the RAG application.
Centralized place for all environment variables and constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# LangSmith Configuration (supports both old and new env var names)
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "true").lower() == "true"
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true"
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT") or os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT") or os.getenv("LANGCHAIN_PROJECT", "corrective-rag-project")

# Set environment variables for LangChain/LangSmith integration
os.environ["LANGSMITH_TRACING"] = str(LANGSMITH_TRACING).lower()
os.environ["LANGCHAIN_TRACING_V2"] = str(LANGCHAIN_TRACING_V2).lower()
os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY or ""
os.environ["LANGSMITH_ENDPOINT"] = LANGSMITH_ENDPOINT
os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT

# Pinecone Configuration
PINECONE_INDEX_NAME = "movie-rag-index"
PINECONE_DIMENSION = 1536  # text-embedding-3-small dimension

# OpenAI Configuration
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"  # GPT-4o-mini (fast and reliable)

# Document Processing
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Settings
TOP_K_RESULTS = 5
RELEVANCE_THRESHOLD = 7.0  # Score must be >= 7/10 to trigger web search (stricter)
MIN_RATING_THRESHOLD = 5.0  # Minimum rating for suggestions (lowered to show more)

# Dataset paths
NETFLIX_CSV = DATA_DIR / "NETFLIX MOVIES AND TV SHOWS CLUSTERING.csv"
TV_SHOWS_CSV = DATA_DIR / "top_rated_2000webseries.csv"
IMDB_MOVIES_CSV = DATA_DIR / "movies_data.csv"
