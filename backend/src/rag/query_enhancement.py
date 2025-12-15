"""
Query Enhancement Module - Improves retrieval through query transformation.

Techniques:
1. HyDE - Generate hypothetical answer, search for that
2. Multi-Query - Generate variations of the query
3. Query Expansion - Add synonyms and related terms
"""

from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.config import OPENAI_API_KEY, CHAT_MODEL


class QueryEnhancer:
    """
    Enhances user queries for better retrieval.

    Why?
    - User queries are often too short or vague
    - Different phrasings retrieve different results
    - Hypothetical answers are semantically closer to documents
    """

    def __init__(self):
        """Initialize LLM for query enhancement."""
        self.llm = ChatOpenAI(
            model=CHAT_MODEL,
            temperature=0.7,  # Slightly creative for variations
            openai_api_key=OPENAI_API_KEY
        )

    def hyde(self, query: str) -> str:
        """
        HyDE: Hypothetical Document Embeddings.

        How it works:
        1. Ask LLM to generate a hypothetical answer
        2. Embed the answer (not the question)
        3. Search for documents similar to the answer

        Why it works:
        - Answers contain keywords similar to actual documents
        - Bridges the semantic gap between questions and documents

        Example:
        Query: "action movies"
        HyDE: "Here are some action movies: Die Hard, The Matrix,
               featuring explosions, car chases..."
        → Search for docs similar to this answer!

        Args:
            query: Original user query

        Returns:
            Hypothetical answer
        """
        hyde_prompt = ChatPromptTemplate.from_template(
            """You are a movie and TV show expert.

Given the user's question, write a hypothetical answer that would appear in our database.
Include specific movie/show titles, genres, actors, and descriptions.

User Question: {query}

Hypothetical Answer (2-3 sentences):"""
        )

        chain = hyde_prompt | self.llm | StrOutputParser()
        hypothetical_answer = chain.invoke({"query": query})

        return hypothetical_answer

    def multi_query(self, query: str, num_variations: int = 3) -> List[str]:
        """
        Generate multiple variations of the same query.

        How it works:
        1. Ask LLM to rephrase the query in different ways
        2. Each variation emphasizes different aspects
        3. Search with all variations and merge results

        Why it works:
        - Different phrasings retrieve different results
        - Covers multiple ways users express the same intent
        - Increases recall (finds more relevant docs)

        Example:
        Query: "funny shows"
        Variations:
        1. "comedy TV series"
        2. "humorous television programs"
        3. "entertaining sitcoms"

        Args:
            query: Original query
            num_variations: Number of variations to generate

        Returns:
            List of query variations (including original)
        """
        multi_query_prompt = ChatPromptTemplate.from_template(
            """You are a helpful assistant that generates multiple variations of a question.

Generate {num_variations} different ways to ask the same question about movies/TV shows.
Each variation should emphasize different aspects or use different terminology.

Original Question: {query}

Variations (one per line):"""
        )

        chain = multi_query_prompt | self.llm | StrOutputParser()
        result = chain.invoke({"query": query, "num_variations": num_variations})

        # Parse variations (assuming one per line)
        variations = [line.strip() for line in result.split('\n') if line.strip()]

        # Add original query
        all_queries = [query] + variations

        return all_queries[:num_variations + 1]  # Ensure we don't exceed limit

    def expand_query(self, query: str) -> str:
        """
        Expand query with synonyms and related terms.

        How it works:
        1. Ask LLM to identify key concepts
        2. Add synonyms and related terms
        3. Create expanded query string

        Why it works:
        - Catches alternative terminology
        - Broadens semantic match
        - Good for recall-focused search

        Example:
        Query: "scary movies"
        Expanded: "scary horror thriller suspense frightening movies films"

        Args:
            query: Original query

        Returns:
            Expanded query with synonyms
        """
        expansion_prompt = ChatPromptTemplate.from_template(
            """You are a query expansion expert for movie/TV databases.

Given a search query, add relevant synonyms and related terms.
Include genre names, similar concepts, and alternative terminology.

Original Query: {query}

Expanded Query (add 3-5 related terms):"""
        )

        chain = expansion_prompt | self.llm | StrOutputParser()
        expanded = chain.invoke({"query": query})

        return expanded
