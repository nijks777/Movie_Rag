# Movie RAG - Intelligent Movie Recommendation System 🎬

Production-ready Retrieval Augmented Generation (RAG) system for movie and TV show recommendations with corrective RAG and web search fallback.

## 🚀 Features

- **Corrective RAG Pipeline** - Self-correcting retrieval with relevance scoring
- **Web Search Fallback** - Tavily API integration when database results are weak
- **Multi-Query Enhancement** - Parallel query variations for better retrieval
- **Smart Recommendations** - Quality filtering (6.5/10+ rating threshold)
- **LangSmith Tracing** - Full observability for LLM calls
- **Modern UI** - Next.js 16 + Tailwind CSS 4 cinema-themed interface

## 📊 Tech Stack

### Backend
- **LangChain** + **LangGraph** - RAG orchestration
- **GPT-4o-mini** - Fast and cost-effective LLM
- **Pinecone** - Serverless vector database (15,446 documents)
- **Tavily API** - AI-optimized web search
- **FastAPI** - High-performance async API
- **LangSmith** - Tracing and monitoring

### Frontend
- **Next.js 16** - React framework with App Router
- **React 19** - Modern UI library
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Utility-first styling

### Data Sources
- Netflix Movies & TV Shows (7,787 titles)
- Top-Rated Web Series (2,000 shows)
- IMDB Indian Movies (5,659 films)

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key
- Pinecone API key
- Tavily API key (optional)
- LangSmith API key (optional)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
# OPENAI_API_KEY=your_key
# PINECONE_API_KEY=your_key
# TAVILY_API_KEY=your_key
# LANGSMITH_API_KEY=your_key

# Run the server
uvicorn src.api.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Access the app at `http://localhost:3000`

## 🎯 RAG Pipeline

```
1. Multi-Query Generation (3 variations)
2. Parallel Execution:
   - RAG: Pinecone vector search + answer generation
   - Web: Tavily search + answer generation
3. Relevance Scoring (0-10 scale)
4. Corrective Combination:
   - Score ≥8.5: Prefer RAG heavily
   - Score 7-8.5: Balanced approach
   - Score <7: Prefer web search
5. Smart Suggestions (Mix RAG 60% + Web 40%)
```

## 📡 API Endpoints

```
GET  /health                - Health check
POST /search                - Basic RAG search
POST /search/corrective     - RAG with web fallback
POST /search/compare        - Compare RAG vs Web results
```

## 🧪 Key Concepts

- **Corrective RAG** - Self-correcting retrieval system
- **Multi-Query Generation** - Query expansion for better recall
- **Parallel Execution** - RAG + Web search run simultaneously
- **Relevance Scoring** - LLM-based quality assessment
- **Quality Filtering** - Only recommend high-rated content
- **LLM Observability** - Full request tracing with LangSmith

## 📚 Project Structure

```
.
├── backend/
│   ├── src/
│   │   ├── api/           # FastAPI endpoints
│   │   ├── rag/           # RAG implementation
│   │   └── config.py      # Configuration
│   └── data/              # CSV datasets (not in repo)
├── frontend/
│   └── app/               # Next.js pages
└── TECH_STACK.md          # Detailed tech documentation
```

## 📄 License

MIT

## 👤 Author

Built by [Jalaj Sharma](https://github.com/nijks777)

---

**Star ⭐ this repo if you find it helpful!**
