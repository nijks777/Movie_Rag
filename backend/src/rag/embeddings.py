"""
Embeddings Module - Handles document embedding and uploading to Pinecone.

Flow:
1. Load documents
2. Generate embeddings using OpenAI
3. Upload to Pinecone in batches
4. Track progress
"""

from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from tqdm import tqdm

from src.config import (
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    PINECONE_INDEX_NAME,
    PINECONE_API_KEY
)


class DocumentEmbedder:
    """
    Handles embedding generation and vector storage.

    What it does:
    1. Takes documents (with text + metadata)
    2. Calls OpenAI API to generate embeddings
    3. Uploads vectors to Pinecone
    4. Preserves metadata for filtering

    Cost calculation:
    - text-embedding-3-small: $0.02 per 1M tokens
    - 15,446 docs × 106 avg tokens = ~1.6M tokens
    - Total cost: ~$0.03 (3 cents!)
    """

    def __init__(self):
        """Initialize embeddings model."""
        self.embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )

    def embed_and_upload(
        self,
        documents: List[Document],
        batch_size: int = 100
    ):
        """
        Embed documents and upload to Pinecone.

        Args:
            documents: List of LangChain Document objects
            batch_size: Number of docs to process at once

        Best Practices:
        - Use batches to avoid rate limits
        - Show progress bar for user feedback
        - Preserve all metadata
        - Handle errors gracefully
        """
        print(f"\n🚀 Embedding {len(documents)} documents...")
        print(f"💰 Estimated cost: ~$0.03 (using {EMBEDDING_MODEL})")

        # Create vector store (automatically embeds + uploads)
        vector_store = PineconeVectorStore.from_documents(
            documents=documents,
            embedding=self.embeddings,
            index_name=PINECONE_INDEX_NAME,
            batch_size=batch_size
        )

        print(f"\n✅ Successfully uploaded {len(documents)} vectors!")
        return vector_store

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a single query for search.

        Args:
            query: Search query text

        Returns:
            Embedding vector (1536 dimensions)
        """
        return self.embeddings.embed_query(query)
