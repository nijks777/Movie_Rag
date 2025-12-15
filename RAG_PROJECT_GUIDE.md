# Corrective RAG Project - 30 Steps (3 Hours)

## Project: Smart Document Q&A with Self-Correction

**Stack**: Python, OpenAI API, Pinecone (free tier), LangChain

## Steps

### Phase 1: Setup (15 min)
1. Create virtual environment and install dependencies
2. Get OpenAI API key
3. Setup Pinecone free account and get API key
4. Create project structure (folders: data, src, notebooks)

### Phase 2: Data Preparation (15 min)
5. Gather 5-10 PDF/text documents (use AI/ML papers or docs)
6. Implement document loader (PDF, TXT, MD)
7. Text chunking with overlap (RecursiveCharacterTextSplitter)
8. Add metadata to chunks (source, page, chunk_id)

### Phase 3: Embeddings & Vector DB (20 min)
9. Initialize OpenAI embeddings (text-embedding-3-small)
10. Create Pinecone index with cosine similarity
11. Generate embeddings for all chunks
12. Upload vectors to Pinecone with metadata

### Phase 4: Basic RAG (20 min)
13. Implement semantic search query
14. Retrieve top-k relevant chunks (k=5)
15. Build basic prompt template
16. Generate answer using GPT-4o-mini
17. Test with 3-5 questions

### Phase 5: Query Enhancement (20 min)
18. Add query rewriting (HyDE - Hypothetical Document Embeddings)
19. Implement multi-query generation (3 variants per question)
20. Add query expansion with synonyms
21. Ensemble retrieval results

### Phase 6: Corrective RAG (30 min)
22. Implement relevance scoring (0-10 scale with LLM)
23. Add fallback: if score < 7, trigger web search (DuckDuckGo/Tavily)
24. Filter irrelevant chunks before generation
25. Implement answer grounding check
26. Add self-reflection: verify answer against sources

### Phase 7: Advanced Features (30 min)
27. Add reranking (cross-encoder or LLM-based)
28. Implement citation tracking (show sources)
29. Add conversation memory (last 3 Q&A pairs)
30. Build streaming response interface

## Key Concepts Covered
- Chunking strategies
- Embeddings & vector similarity
- Semantic search
- Prompt engineering
- Query transformation
- Retrieval evaluation
- Self-correction mechanisms
- Reranking
- Citation & grounding
- Conversational context

## Deliverables
- Working Corrective RAG system
- Jupyter notebook with examples
- Comparison: Basic RAG vs Corrective RAG
- Performance metrics (relevance, latency)

## Success Criteria
- Answer accuracy > 85%
- Proper source citation
- Self-correction on poor retrieval
- Response time < 5 seconds
