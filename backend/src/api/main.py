"""
FastAPI Backend for Corrective RAG System.

Endpoints:
- GET  /health                    - Health check
- POST /search                    - Basic RAG search
- POST /search/corrective         - Corrective RAG with web fallback
- POST /search/compare            - Compare RAG vs Web results
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.rag.corrective_rag import CorrectiveRAG

# Initialize FastAPI app
app = FastAPI(
    title="Movie RAG API",
    description="Corrective RAG system for movie and TV show recommendations",
    version="1.0.0"
)

# CORS middleware - allows frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system (singleton)
rag_system = None


def get_rag_system():
    """Lazy load RAG system (expensive initialization)."""
    global rag_system
    if rag_system is None:
        print("🔄 Initializing RAG system...")
        rag_system = CorrectiveRAG()
        print("✅ RAG system ready!")
    return rag_system


# Request/Response Models
class SearchRequest(BaseModel):
    """Search request payload."""
    query: str
    strategy: Optional[str] = "multi_query"  # basic, hyde, multi_query, expansion
    k: Optional[int] = 5


class SearchResponse(BaseModel):
    """Search response payload."""
    question: str
    answer: str
    sources: List[Dict]
    metadata: Optional[Dict] = None


class CompareRequest(BaseModel):
    """Compare request payload."""
    query: str
    k: Optional[int] = 3


class CompareResponse(BaseModel):
    """Compare response payload."""
    query: str
    rag_result: Dict
    web_result: Dict
    combined_answer: str
    suggestions: Optional[List[Dict]] = None


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Movie RAG API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "rag_initialized": rag_system is not None
    }


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Basic RAG search (no web fallback).

    Example:
    POST /search
    {
        "query": "action movies",
        "strategy": "multi_query",
        "k": 5
    }
    """
    try:
        rag = get_rag_system()

        # Use enhanced RAG (no web fallback)
        result = rag.query_enhanced(
            question=request.query,
            strategy=request.strategy,
            k=request.k
        )

        return SearchResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"],
            metadata={
                "strategy": result.get("strategy"),
                "num_sources": result.get("num_sources")
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search/corrective", response_model=SearchResponse)
async def search_corrective(request: SearchRequest):
    """
    Corrective RAG search with web fallback.

    Automatically triggers web search if relevance score is low.

    Example:
    POST /search/corrective
    {
        "query": "Who won the Oscar in 2024?",
        "strategy": "basic",
        "k": 3
    }
    """
    try:
        rag = get_rag_system()

        # Use corrective RAG (with web fallback)
        result = rag.query_corrective(
            question=request.query,
            strategy=request.strategy,
            k=request.k,
            enable_web_fallback=True,
            enable_verification=True
        )

        return SearchResponse(
            question=result["question"],
            answer=result["answer"],
            sources=result["sources"],
            metadata=result["metadata"]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search/compare", response_model=CompareResponse)
async def search_compare(request: CompareRequest):
    """
    Compare RAG vs Web search results with TRUE parallel execution.

    Returns both results side-by-side with a combined answer.

    Example:
    POST /search/compare
    {
        "query": "funny Indian shows",
        "k": 3
    }
    """
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    try:
        rag = get_rag_system()

        # STEP 1: Run RAG + Web Search in PARALLEL (truly parallel)
        executor = ThreadPoolExecutor(max_workers=2)

        def run_rag():
            return rag.query_enhanced(
                question=request.query,
                strategy="multi_query",  # Generate 3 query variations
                k=request.k
            )

        def run_web():
            web_docs = rag.web_search_fallback(request.query)
            if not web_docs:
                return None, []

            web_context = rag.format_docs(web_docs)
            web_answer = rag.generate_answer(request.query, web_context)

            web_sources = []
            for doc in web_docs[:5]:
                web_sources.append({
                    "title": doc.metadata.get('title', 'Web Result'),
                    "source": doc.metadata.get('url', 'Tavily')
                })

            return web_answer, web_sources

        # Run both in parallel
        loop = asyncio.get_event_loop()
        rag_future = loop.run_in_executor(executor, run_rag)
        web_future = loop.run_in_executor(executor, run_web)

        # Wait for both to complete
        rag_result, (web_answer, web_sources) = await asyncio.gather(rag_future, web_future)

        # STEP 2: Score RAG relevance (only 1 LLM call)
        docs = [doc for doc in rag.retrieve(request.query, k=request.k)]
        relevance_score, _ = rag.score_relevance(request.query, docs)

        # STEP 3: Corrective RAG - Intelligent combination
        # HIGH score (>=8.5) = RAG is excellent, prefer RAG heavily
        # GOOD score (7-8.5) = RAG is good, balanced approach
        # LOW score (<7) = RAG is weak, prefer web heavily

        if web_answer:
            if relevance_score >= 8.5:
                # RAG is excellent, give it strong preference
                combined_prompt = f"""Give a SHORT conversational answer (2-3 sentences). Recommend ONE movie rated 6.5/10+. Don't list multiple movies.

Database (HIGHLY RELEVANT - Prefer this): {rag_result['answer']}
Web (Additional context): {web_answer}

Short conversational answer (prefer database recommendation):"""
            elif relevance_score >= 7.0:
                # Both are good, balanced combination
                combined_prompt = f"""Give a SHORT conversational answer (2-3 sentences). Recommend ONE movie rated 6.5/10+. Don't list multiple movies.

Database: {rag_result['answer']}
Web: {web_answer}

Short conversational answer (combine both sources):"""
            else:
                # RAG is weak, prefer web
                combined_prompt = f"""Give a SHORT conversational answer (2-3 sentences). Recommend ONE movie rated 6.5/10+. Don't list multiple movies.

Web (PRIMARY - Prefer this): {web_answer}
Database (Additional context): {rag_result['answer']}

Short conversational answer (prefer web recommendation):"""

            final_answer = rag.llm.invoke(combined_prompt).content
        else:
            final_answer = rag_result["answer"]

        # STEP 4: Get suggestions - Mix RAG + Web results for diversity
        rag_suggestions = rag.get_movie_suggestions(request.query, num_suggestions=10)

        # Extract actual movie names from web search content
        web_suggestions = []
        if web_answer:
            # Use LLM to extract movie names from web content
            extract_prompt = f"""Extract ONLY movie/show titles from this text. Return a simple list of titles, one per line. No explanations.

Text: {web_answer}

Movie titles (one per line):"""

            extracted = rag.llm.invoke(extract_prompt).content
            web_movie_titles = [
                line.strip().lstrip('-').lstrip('*').lstrip('•').strip()
                for line in extracted.split('\n')
                if line.strip() and len(line.strip()) > 3
            ]

            # Create suggestions from extracted titles
            for title in web_movie_titles[:5]:
                if title:
                    web_suggestions.append({
                        "title": title,
                        "genre": "Web Pick",
                        "rating": "Fresh",
                        "source": "web",
                        "year": "2024"
                    })

        # Mix RAG (60%) + Web (40%) suggestions for best of both
        mixed_suggestions = []
        seen_titles_lower = set()

        # Add top RAG results first (higher quality from our DB)
        for sug in rag_suggestions[:3]:
            title_lower = sug['title'].lower()
            if title_lower not in seen_titles_lower:
                mixed_suggestions.append(sug)
                seen_titles_lower.add(title_lower)

        # Add web movie titles for diversity
        for sug in web_suggestions[:2]:
            title_lower = sug['title'].lower()
            if title_lower not in seen_titles_lower:
                mixed_suggestions.append(sug)
                seen_titles_lower.add(title_lower)

        # Fill remaining slots with RAG results
        for sug in rag_suggestions[3:]:
            if len(mixed_suggestions) >= 5:
                break
            title_lower = sug['title'].lower()
            if title_lower not in seen_titles_lower:
                mixed_suggestions.append(sug)
                seen_titles_lower.add(title_lower)

        return CompareResponse(
            query=request.query,
            rag_result={
                "answer": rag_result["answer"],
                "sources": rag_result["sources"][:3],
                "num_sources": len(rag_result["sources"])
            },
            web_result={
                "answer": web_answer if web_answer else "",
                "sources": web_sources,
                "num_sources": len(web_sources)
            },
            combined_answer=final_answer,
            suggestions=mixed_suggestions[:5]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Run with: uvicorn src.api.main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
