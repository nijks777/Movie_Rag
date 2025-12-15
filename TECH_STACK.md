# Corrective RAG Movie Recommendation System - Tech Stack

## Project Overview
Intelligent movie recommendation system using Retrieval Augmented Generation (RAG) with web search fallback and quality filtering.

---

## 🔧 Backend Technologies

### AI/ML Framework
- **LangChain** - RAG orchestration framework
- **LangGraph** - Advanced workflow management
- **LangSmith** - LLM observability and tracing

### Large Language Models
- **GPT-5 Nano** (`gpt-5-nano-2025-08-07`) - Latest OpenAI model for response generation
- **OpenAI Embeddings** (`text-embedding-3-small`) - 1536-dim vector embeddings

### Vector Database
- **Pinecone** - Serverless vector database for semantic search
  - Cosine similarity search
  - 15,446 movie/TV documents indexed

### Web Search
- **Tavily API** - AI-optimized web search engine for corrective RAG

### API Framework
- **FastAPI** - High-performance async Python web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

### Data Processing
- **Pandas** - CSV data processing
- **Python 3.13** - Core programming language

---

## 🎨 Frontend Technologies

### Framework & Libraries
- **Next.js 16** - React framework with App Router
- **React 19.2** - UI component library
- **TypeScript 5** - Type-safe JavaScript

### Styling
- **Tailwind CSS 4** - Utility-first CSS framework
- **Custom Theme** - Cinema-inspired black/white/gold design system

### Build Tools
- **Turbopack** - Next-gen bundler (Next.js default)
- **PostCSS** - CSS processing

---

## 📊 Data Sources

### Datasets (15,446 documents)
1. **Netflix Movies & TV Shows** - 7,787 titles
2. **Top-Rated Web Series** - 2,000 shows
3. **IMDB Indian Movies** - 5,659 films

### Data Pipeline
- CSV ingestion
- Metadata extraction (title, genre, rating, cast, year)
- Vector embedding generation
- Pinecone indexing

---

## 🧠 RAG Architecture

### Query Enhancement Strategies
1. **Basic** - Direct similarity search
2. **HyDE** (Hypothetical Document Embeddings)
3. **Multi-Query** - Generate query variations
4. **Query Expansion** - Add synonyms/related terms

### Corrective RAG Pipeline
1. **Vector Search** - Retrieve from 15K movie database
2. **Relevance Scoring** - LLM rates relevance (0-10 scale)
3. **Web Fallback** - Tavily search when score < 7.0
4. **Answer Synthesis** - Combine DB + web results
5. **Quality Filter** - Only recommend movies rated ≥ 6.5/10

### Key Features
- **Self-correction** - Detects low-quality results
- **Web augmentation** - Fresh information from Tavily
- **Answer verification** - Grounding check
- **Quality filtering** - Rating-based recommendations

---

## 🔗 API Endpoints

```
GET  /health                - Health check
POST /search                - Basic RAG search
POST /search/corrective     - RAG with web fallback
POST /search/compare        - Compare RAG vs Web
```

---

## 📦 Key Python Packages

```
langchain                   - RAG framework
langchain-openai            - OpenAI integration
langchain-pinecone          - Pinecone vector store
langchain-community         - Community tools
langgraph                   - Workflow graphs
langsmith                   - Tracing/monitoring
pinecone-client             - Vector database client
tavily-python               - Web search
fastapi                     - Web framework
pydantic                    - Data validation
pandas                      - Data processing
python-dotenv               - Environment management
```

---

## 🎯 Resume-Friendly Tech Summary

**Full-Stack AI Application:**
- Built production-ready RAG system using **LangChain**, **GPT-5 Nano**, and **Pinecone**
- Implemented **Corrective RAG** with web search fallback using **Tavily API**
- Deployed **FastAPI** backend + **Next.js 16/React 19** frontend with **TypeScript**
- Integrated **LangSmith** for LLM observability and tracing
- Processed 15K+ documents with **OpenAI embeddings** and vector search
- Applied advanced retrieval strategies (HyDE, Multi-Query, Query Expansion)
- Built responsive UI with **Tailwind CSS 4** and custom design system

**Key Skills Demonstrated:**
- RAG/LLM Engineering
- Vector Databases (Pinecone)
- API Development (FastAPI)
- Modern React (Next.js 16, TypeScript)
- AI Orchestration (LangChain, LangGraph)
- Prompt Engineering
- Full-Stack Development

---

## 🚀 Performance Optimizations

1. **Fast Query Strategy** - Basic search for speed
2. **Lazy Loading** - RAG system initialized on first request
3. **Quality Filtering** - Pre-filter low-rated movies
4. **Efficient Prompts** - Minimal token usage
5. **Async Operations** - Non-blocking I/O

---

## 📈 Monitoring & Observability

- **LangSmith** integration for request tracing
- **Health checks** for service monitoring
- Project: `corrective-rag-project`
- View traces at: https://smith.langchain.com

---

## 🔐 Environment Variables

```env
OPENAI_API_KEY              # GPT-5 Nano access
PINECONE_API_KEY            # Vector DB access
TAVILY_API_KEY              # Web search access
LANGCHAIN_API_KEY           # LangSmith tracing
LANGCHAIN_TRACING_V2=true   # Enable tracing
```

---

## 📝 Project Highlights

✅ **15,446 documents** indexed with semantic search
✅ **Quality-first** recommendations (≥6.5/10 rating filter)
✅ **Web-augmented** answers via Tavily API
✅ **Self-correcting** pipeline with relevance scoring
✅ **Production-ready** with FastAPI + Next.js
✅ **Observable** with LangSmith tracing
✅ **Modern stack** - GPT-5, React 19, Tailwind 4

---

**GitHub-Ready Description:**
*"Intelligent movie recommendation system built with LangChain, GPT-5 Nano, and Pinecone. Features corrective RAG with web search fallback, quality filtering, and modern Next.js frontend. Processes 15K+ movies with advanced retrieval strategies (HyDE, Multi-Query). Includes LangSmith observability and FastAPI backend."*
