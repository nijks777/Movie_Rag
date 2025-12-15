"""
Basic RAG Pipeline - Retrieval Augmented Generation.

Flow:
1. User asks a question
2. Embed the question
3. Retrieve top-K similar documents from Pinecone
4. Build prompt with question + context
5. Generate answer using GPT-4o-mini
6. Return answer with sources
"""

from typing import List, Dict
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from src.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    CHAT_MODEL,
    PINECONE_INDEX_NAME,
    TOP_K_RESULTS
)
from src.rag.prompts import basic_rag_prompt, rag_with_sources_prompt


class BasicRAG:
    """
    Basic RAG implementation.

    What it does:
    1. Takes user question
    2. Finds relevant movies/shows (semantic search)
    3. Generates answer using LLM
    4. Returns answer with sources
    """

    def __init__(self):
        """Initialize RAG components."""
        # Embeddings for query encoding
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )

        # Vector store for retrieval
        self.vector_store = PineconeVectorStore(
            index_name=PINECONE_INDEX_NAME,
            embedding=self.embeddings
        )

        # LLM for answer generation
        self.llm = ChatOpenAI(
            model=CHAT_MODEL,
            temperature=0,  # Deterministic answers
            openai_api_key=OPENAI_API_KEY
        )

    def retrieve(self, query: str, k: int = TOP_K_RESULTS) -> List[Document]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: User question
            k: Number of documents to retrieve

        Returns:
            List of relevant Document objects
        """
        return self.vector_store.similarity_search(query, k=k)

    def format_docs(self, docs: List[Document]) -> str:
        """
        Format retrieved documents into context string.

        Args:
            docs: List of retrieved documents

        Returns:
            Formatted context string
        """
        context_parts = []

        for i, doc in enumerate(docs, 1):
            title = doc.metadata.get('title', 'Unknown')
            source = doc.metadata.get('source', 'Unknown')
            genre = doc.metadata.get('genre', 'Unknown')
            rating = doc.metadata.get('rating', 'Unknown')

            context_part = f"""
Document {i}:
Title: {title}
Source: {source}
Genre: {genre}
Rating: {rating}
Content: {doc.page_content}
"""
            context_parts.append(context_part.strip())

        return "\n\n---\n\n".join(context_parts)

    def generate_answer(self, question: str, context: str) -> str:
        """
        Generate answer using LLM.

        Args:
            question: User question
            context: Retrieved context

        Returns:
            Generated answer
        """
        # Build chain: prompt → LLM → parse output
        chain = (
            {"context": lambda x: context, "question": lambda x: question}
            | rag_with_sources_prompt
            | self.llm
            | StrOutputParser()
        )

        return chain.invoke({})

    def query(self, question: str, k: int = TOP_K_RESULTS) -> Dict:
        """
        Complete RAG pipeline: retrieve + generate.

        Args:
            question: User question
            k: Number of documents to retrieve

        Returns:
            Dictionary with answer and sources
        """
        print(f"🔍 Retrieving relevant documents...")

        # Step 1: Retrieve relevant documents
        docs = self.retrieve(question, k=k)

        print(f"✅ Found {len(docs)} relevant documents")
        print(f"🤖 Generating answer...")

        # Step 2: Format context
        context = self.format_docs(docs)

        # Step 3: Generate answer
        answer = self.generate_answer(question, context)

        # Step 4: Prepare response
        response = {
            "question": question,
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

    def query_simple(self, question: str, k: int = TOP_K_RESULTS) -> str:
        """
        Simple query interface - returns just the answer.

        Args:
            question: User question
            k: Number of documents to retrieve

        Returns:
            Generated answer string
        """
        result = self.query(question, k=k)
        return result["answer"]
