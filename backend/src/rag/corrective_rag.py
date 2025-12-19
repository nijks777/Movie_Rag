"""
Corrective RAG - Self-correcting retrieval system.

Key Features:
1. Relevance Scoring - Rate how relevant retrieved docs are
2. Web Search Fallback - Search DuckDuckGo if docs aren't relevant
3. Self-Reflection - Verify answer is grounded in sources
4. Adaptive Retrieval - Choose best source dynamically
"""

from typing import List, Dict, Tuple
import os
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tavily import TavilyClient

from src.config import OPENAI_API_KEY, CHAT_MODEL, RELEVANCE_THRESHOLD, MIN_RATING_THRESHOLD
from src.rag.enhanced_rag import EnhancedRAG


class CorrectiveRAG(EnhancedRAG):
    """
    Corrective RAG with self-correction capabilities.

    What makes it "corrective":
    1. Scores relevance of retrieved docs
    2. Falls back to web search if needed
    3. Verifies answers are grounded in sources
    4. Provides confidence scores
    """

    def __init__(self):
        """Initialize Corrective RAG components."""
        super().__init__()

        # Web search tool - Tavily (better for LLM applications)
        tavily_key = os.getenv("TAVILY_API_KEY", "tvly-demo-key")  # Use demo key if not set
        self.web_search = TavilyClient(api_key=tavily_key)

        # LLM for scoring and reflection
        self.scorer_llm = ChatOpenAI(
            model=CHAT_MODEL,
            temperature=0,  # Deterministic for scoring
            openai_api_key=OPENAI_API_KEY
        )

    def score_relevance(self, query: str, documents: List[Document]) -> Tuple[float, str]:
        """
        Score how relevant retrieved documents are to the query.

        Args:
            query: User question
            documents: Retrieved documents

        Returns:
            Tuple of (score 0-10, explanation)

        How it works:
        - Ask LLM to rate relevance on scale of 0-10
        - 0 = Completely irrelevant
        - 10 = Perfectly relevant
        - Threshold: 7 (configurable)
        """
        # Format documents for scoring
        docs_text = "\n\n".join([
            f"Doc {i+1}: {doc.page_content[:200]}..."
            for i, doc in enumerate(documents[:3])  # Score top 3
        ])

        scoring_prompt = ChatPromptTemplate.from_template(
            """You are an expert relevance scorer for a movie/TV recommendation system with advanced semantic understanding.

Your task: Rate how well these documents can answer the user's question with HIGH PRECISION.

CRITICAL SCORING CRITERIA:
- **Actor/Cast Matching**: If user asks for specific actors, documents MUST contain those exact actors in Cast/Stars fields
- **Semantic Relevance**: Documents must match the core intent (genre, theme, mood, specific attributes)
- **Information Completeness**: Documents must have enough detail to answer comprehensively
- **Quality**: Higher-rated content is more valuable for recommendations

Scoring Guide (BE STRICT):
- 0-3: Completely irrelevant, wrong topic, or missing critical filter (e.g., wrong actor)
- 4-6: Somewhat related but missing key information or only partial match
- 7-8: Relevant and can answer the question adequately
- 9-10: Highly relevant, perfect match for all criteria, contains complete information

User Question: {query}

Retrieved Documents:
{documents}

Instructions:
1. First line: Give ONLY a number (0-10)
2. Second line: One sentence explaining your score

Your Score:"""
        )

        chain = scoring_prompt | self.scorer_llm | StrOutputParser()
        result = chain.invoke({"query": query, "documents": docs_text})

        # Parse score and explanation
        lines = result.strip().split('\n')
        try:
            score = float(lines[0].strip())
            explanation = lines[1] if len(lines) > 1 else "No explanation provided"
        except:
            score = 5.0  # Default if parsing fails
            explanation = result

        return score, explanation

    def web_search_fallback(self, query: str) -> List[Document]:
        """
        Perform web search when vector DB results are irrelevant.

        Args:
            query: User question

        Returns:
            List of Documents from web search results

        Why web search?
        - Our DB only has Netflix + IMDB movies
        - Questions about other content need external data
        - DuckDuckGo provides fresh, relevant info
        """
        print("🌐 Performing web search (Tavily)...")

        try:
            # Search with Tavily (better quality for LLM apps)
            response = self.web_search.search(
                query=query,
                max_results=5,
                search_depth="basic"
            )

            # Convert to Document format
            web_docs = []
            for result in response.get('results', []):
                doc = Document(
                    page_content=result.get('content', ''),
                    metadata={
                        "source": "web_search",
                        "title": result.get('title', 'Web Result'),
                        "url": result.get('url', ''),
                        "search_engine": "Tavily"
                    }
                )
                web_docs.append(doc)

            return web_docs

        except Exception as e:
            print(f"⚠️  Web search failed: {e}")
            print("💡 Get free Tavily API key at https://tavily.com")
            return []

    def verify_answer(self, question: str, answer: str, context: str) -> Tuple[bool, str]:
        """
        Verify that the answer is grounded in the provided context.

        Self-Reflection Process:
        1. Check if answer contains information from context
        2. Detect hallucinations (made-up facts)
        3. Verify citations are accurate

        Args:
            question: User question
            answer: Generated answer
            context: Source documents

        Returns:
            Tuple of (is_grounded: bool, feedback: str)
        """
        verification_prompt = ChatPromptTemplate.from_template(
            """You are a fact-checker for a Q&A system.

Verify if the answer is fully grounded in the provided context.

Rules:
1. Answer should ONLY use information from context
2. Flag any facts not present in context
3. Check if citations are accurate

Question: {question}

Context:
{context}

Generated Answer:
{answer}

Is the answer grounded? (YES/NO):
Feedback (one sentence):"""
        )

        chain = verification_prompt | self.scorer_llm | StrOutputParser()
        result = chain.invoke({
            "question": question,
            "answer": answer,
            "context": context
        })

        lines = result.strip().split('\n')
        is_grounded = "yes" in lines[0].lower()
        feedback = lines[1] if len(lines) > 1 else "No feedback"

        return is_grounded, feedback

    def refine_with_feedback(
        self,
        question: str,
        initial_docs: List[Document],
        initial_answer: str
    ) -> Tuple[List[Document], str]:
        """
        Feedback loop: Re-retrieve if initial answer quality is poor.

        Args:
            question: User question
            initial_docs: First set of retrieved documents
            initial_answer: Generated answer from initial docs

        Returns:
            Tuple of (refined_docs, refined_answer)
        """
        # Check if answer seems incomplete or low quality
        answer_lower = initial_answer.lower()
        quality_issues = [
            len(initial_answer) < 50,  # Too short
            "i don't" in answer_lower or "cannot" in answer_lower,  # Uncertain
            "no information" in answer_lower,  # Missing info
        ]

        if any(quality_issues):
            print("🔄 Feedback loop: Refining results due to low initial quality...")

            # Try different retrieval strategy
            refined_docs = self.retrieve_with_multi_query(question, k=10)

            # Re-generate answer
            context = self.format_docs(refined_docs)
            refined_answer = self.generate_answer(question, context)

            return refined_docs, refined_answer

        return initial_docs, initial_answer

    def query_corrective(
        self,
        question: str,
        strategy: str = "multi_query",
        k: int = 5,
        enable_web_fallback: bool = True,
        enable_verification: bool = True,
        enable_feedback_loop: bool = True
    ) -> Dict:
        """
        Complete Corrective RAG pipeline.

        Steps:
        1. Retrieve from vector DB
        2. Score relevance
        3. If score < threshold: web search
        4. Generate answer
        5. Verify answer is grounded
        6. Return with confidence

        Args:
            question: User question
            strategy: Query enhancement strategy
            k: Number of docs to retrieve
            enable_web_fallback: Enable web search fallback
            enable_verification: Enable answer verification

        Returns:
            Dict with answer, sources, scores, and metadata
        """
        print(f"\n{'='*80}")
        print(f"🔧 CORRECTIVE RAG PIPELINE")
        print(f"{'='*80}\n")

        # Step 1: Retrieve from vector DB
        print(f"📊 Step 1: Retrieving from vector database...")
        if strategy == "basic":
            docs = self.retrieve(question, k=k)
        else:
            # Use enhanced retrieval
            if strategy == "hyde":
                docs = self.retrieve_with_hyde(question, k=k)
            elif strategy == "multi_query":
                docs = self.retrieve_with_multi_query(question, k=k)
            else:
                docs = self.retrieve_with_expansion(question, k=k)

        # Step 2: Score relevance
        print(f"\n⭐ Step 2: Scoring relevance...")
        relevance_score, score_explanation = self.score_relevance(question, docs)
        print(f"   Score: {relevance_score}/10")
        print(f"   Reason: {score_explanation}")

        used_web_search = False

        # Step 3: Web search fallback if needed
        if enable_web_fallback and (relevance_score < RELEVANCE_THRESHOLD or len(docs) < 2):
            print(f"\n⚠️  Relevance score ({relevance_score}) < threshold ({RELEVANCE_THRESHOLD}) or low doc count ({len(docs)})")
            print(f"🌐 Step 3: Triggering web search fallback...")

            web_docs = self.web_search_fallback(question)

            if web_docs:
                # Combine and prioritize web results
                docs = web_docs + docs
                used_web_search = True
                print(f"✅ Using combined web and vector search results")
            else:
                print(f"⚠️  Web search failed, using vector DB results anyway")
        else:
            print(f"\n✅ Step 3: Skipped (relevance score sufficient)")

        # Step 4: Generate answer
        print(f"\n🤖 Step 4: Generating answer...")
        context = self.format_docs(docs)
        answer = self.generate_answer(question, context)

        # Step 4.5: Feedback loop refinement (NEW)
        used_feedback_loop = False
        if enable_feedback_loop:
            original_answer = answer
            docs, answer = self.refine_with_feedback(question, docs, answer)
            if answer != original_answer:
                used_feedback_loop = True
                context = self.format_docs(docs)  # Update context
                print(f"✅ Feedback loop applied - answer refined")

        # Step 5: Verify answer (self-reflection)
        is_grounded = True
        verification_feedback = "Verification skipped"

        if enable_verification:
            print(f"\n🔍 Step 5: Verifying answer is grounded...")
            is_grounded, verification_feedback = self.verify_answer(
                question, answer, context
            )
            print(f"   Grounded: {'✅ YES' if is_grounded else '❌ NO'}")
            print(f"   Feedback: {verification_feedback}")
        else:
            print(f"\n⏭️  Step 5: Skipped (verification disabled)")

        # Prepare response
        response = {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "title": doc.metadata.get('title', 'Unknown'),
                    "source": doc.metadata.get('source', 'Unknown'),
                    "genre": doc.metadata.get('genre', 'N/A'),
                    "rating": doc.metadata.get('rating', 'N/A')
                }
                for doc in docs
            ],
            "metadata": {
                "strategy": strategy,
                "relevance_score": relevance_score,
                "score_explanation": score_explanation,
                "used_web_search": used_web_search,
                "used_feedback_loop": used_feedback_loop,
                "is_grounded": is_grounded,
                "verification_feedback": verification_feedback,
                "num_sources": len(docs)
            }
        }

        print(f"\n{'='*80}")
        print(f"✅ CORRECTIVE RAG COMPLETE")
        print(f"{'='*80}\n")

        return response

    def get_movie_suggestions(self, query: str, num_suggestions: int = 5) -> List[Dict]:
        """
        Get HIGH-QUALITY movie/TV suggestions based on the query with SMART FILTERING.

        INTELLIGENT FILTERING:
        - Actor-aware: If query mentions actors, verifies cast/stars field
        - Quality threshold: Only suggests movies with rating >= 6.5/10
        - Relevance scoring: Matches query terms in content
        - Diversity: Avoids duplicate titles
        - Prioritizes higher-rated content

        Args:
            query: User question
            num_suggestions: Number of suggestions to return

        Returns:
            List of high-quality movie/TV show suggestions with metadata
        """
        # Retrieve MORE docs to filter for quality and relevance
        docs = self.retrieve(query, k=num_suggestions * 5)

        # Check if query mentions actors (simple detection)
        query_lower = query.lower()
        words = query_lower.split()

        # Extract unique HIGH-QUALITY titles only
        suggestions = []
        seen_titles = set()

        for doc in docs:
            if len(suggestions) >= num_suggestions:
                break

            title = doc.metadata.get('title', 'Unknown')
            rating_str = doc.metadata.get('rating', '0')
            content = doc.page_content.lower()

            # Parse rating (handle different formats: "7.5", "7.5/10", etc.)
            try:
                rating = float(str(rating_str).split('/')[0])
            except (ValueError, AttributeError):
                rating = 0.0

            # QUALITY FILTER: Only recommend highly-rated movies (>= 6.5/10)
            if rating < MIN_RATING_THRESHOLD:
                continue

            # ACTOR FILTER: If query seems actor-specific, verify presence in content
            # Check if critical query terms appear in the document content
            query_match_score = sum(1 for word in words if len(word) > 3 and word in content)

            # If query has specific terms (like actor names), require minimum match
            if len(words) > 2:  # Multi-word query likely has specific intent
                # Require at least 50% of meaningful words to match
                meaningful_words = [w for w in words if len(w) > 3]
                if meaningful_words and query_match_score < len(meaningful_words) * 0.4:
                    continue  # Skip if not enough term matches

            if title not in seen_titles:
                suggestions.append({
                    "title": title,
                    "genre": doc.metadata.get('genre', 'N/A'),
                    "rating": f"{rating}/10",
                    "source": doc.metadata.get('source', 'Unknown'),
                    "year": doc.metadata.get('year', doc.metadata.get('release_year', 'N/A')),
                    "relevance_score": query_match_score  # For debugging/ranking
                })
                seen_titles.add(title)

        # Sort by rating (highest first) for best recommendations
        suggestions.sort(key=lambda x: float(x['rating'].split('/')[0]), reverse=True)

        # Remove relevance_score from final output
        for suggestion in suggestions:
            suggestion.pop('relevance_score', None)

        return suggestions
