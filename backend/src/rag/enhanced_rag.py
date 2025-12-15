"""
Enhanced RAG Pipeline with Query Enhancement.

Combines:
1. Basic RAG
2. HyDE (Hypothetical Document Embeddings)
3. Multi-Query generation
4. Query Expansion

Allows switching between strategies.
"""

from typing import List, Dict
from langchain_core.documents import Document

from src.rag.basic_rag import BasicRAG
from src.rag.query_enhancement import QueryEnhancer


class EnhancedRAG(BasicRAG):
    """
    Enhanced RAG with query transformation strategies.

    Extends BasicRAG with:
    - HyDE for better semantic matching
    - Multi-query for broader coverage
    - Query expansion for recall
    """

    def __init__(self):
        """Initialize enhanced RAG components."""
        super().__init__()
        self.query_enhancer = QueryEnhancer()

    def retrieve_with_hyde(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve using HyDE strategy.

        Steps:
        1. Generate hypothetical answer
        2. Embed the answer
        3. Search for similar documents

        Args:
            query: User question
            k: Number of docs to retrieve

        Returns:
            List of relevant documents
        """
        print(f"🔮 Using HyDE strategy...")

        # Generate hypothetical answer
        hypothetical_answer = self.query_enhancer.hyde(query)
        print(f"💭 Hypothetical answer: {hypothetical_answer[:100]}...")

        # Search using the hypothetical answer
        docs = self.vector_store.similarity_search(hypothetical_answer, k=k)

        return docs

    def retrieve_with_multi_query(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve using multi-query strategy with PARALLEL searches.

        Steps:
        1. Generate 3 query variations
        2. Search with each variation IN PARALLEL
        3. Merge and deduplicate results

        Args:
            query: User question
            k: Total number of docs to retrieve

        Returns:
            Merged list of relevant documents
        """
        from concurrent.futures import ThreadPoolExecutor

        print(f"🔀 Using Multi-Query strategy...")

        # Generate query variations
        queries = self.query_enhancer.multi_query(query, num_variations=3)
        print(f"📝 Generated {len(queries)} query variations")

        # Retrieve from each query IN PARALLEL
        per_query_k = max(2, k // len(queries))  # Split k across queries

        def search_query(q_tuple):
            i, q = q_tuple
            print(f"   {i}. '{q}'")
            return self.vector_store.similarity_search(q, k=per_query_k)

        # Run all 3 searches in parallel (much faster!)
        with ThreadPoolExecutor(max_workers=3) as executor:
            query_results = list(executor.map(search_query, enumerate(queries, 1)))

        # Merge and deduplicate results
        all_docs = []
        seen_titles = set()

        for docs in query_results:
            for doc in docs:
                title = doc.metadata.get('title', '')
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    all_docs.append(doc)

        # Return top k unique docs
        return all_docs[:k]

    def retrieve_with_expansion(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve using query expansion.

        Steps:
        1. Expand query with synonyms
        2. Search with expanded query

        Args:
            query: User question
            k: Number of docs to retrieve

        Returns:
            List of relevant documents
        """
        print(f"➕ Using Query Expansion strategy...")

        # Expand query
        expanded_query = self.query_enhancer.expand_query(query)
        print(f"📝 Expanded query: {expanded_query}")

        # Search with expanded query
        docs = self.vector_store.similarity_search(expanded_query, k=k)

        return docs

    def query_enhanced(
        self,
        question: str,
        strategy: str = "multi_query",
        k: int = 5
    ) -> Dict:
        """
        Complete enhanced RAG pipeline.

        Args:
            question: User question
            strategy: Enhancement strategy
                     - "basic": No enhancement
                     - "hyde": Hypothetical Document Embeddings
                     - "multi_query": Multiple query variations
                     - "expansion": Query expansion with synonyms
            k: Number of documents to retrieve

        Returns:
            Dictionary with answer and sources
        """
        print(f"\n🎯 Strategy: {strategy.upper()}")
        print(f"🔍 Retrieving relevant documents...\n")

        # Choose retrieval strategy
        if strategy == "hyde":
            docs = self.retrieve_with_hyde(question, k=k)
        elif strategy == "multi_query":
            docs = self.retrieve_with_multi_query(question, k=k)
        elif strategy == "expansion":
            docs = self.retrieve_with_expansion(question, k=k)
        else:  # basic
            docs = self.retrieve(question, k=k)

        print(f"\n✅ Found {len(docs)} relevant documents")
        print(f"🤖 Generating answer...\n")

        # Format context
        context = self.format_docs(docs)

        # Generate answer
        answer = self.generate_answer(question, context)

        # Prepare response
        response = {
            "question": question,
            "strategy": strategy,
            "answer": answer,
            "sources": [
                {
                    "title": doc.metadata.get('title', 'Unknown'),
                    "source": doc.metadata.get('source', 'Unknown'),
                    "genre": doc.metadata.get('genre', 'Unknown'),
                    "rating": doc.metadata.get('rating', 'Unknown')
                }
                for doc in docs
            ],
            "num_sources": len(docs)
        }

        return response
