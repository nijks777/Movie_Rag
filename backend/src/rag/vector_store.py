"""
Vector Store Module - Handles Pinecone index creation and management.

What this does:
1. Creates a Pinecone index (if not exists)
2. Manages index configuration (dimension, metric, cloud)
3. Provides utilities for index operations
"""

import time
from pinecone import Pinecone, ServerlessSpec
from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_DIMENSION


class PineconeVectorStore:
    """
    Manages Pinecone vector database operations.

    Best Practices:
    1. Check if index exists before creating
    2. Use serverless spec for cost-efficiency
    3. Choose cosine similarity for text embeddings
    4. Wait for index to be ready before using
    """

    def __init__(self):
        """Initialize Pinecone client."""
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index_name = PINECONE_INDEX_NAME

    def create_index(self):
        """
        Create a Pinecone index if it doesn't exist.

        Index Configuration:
        - Dimension: 1536 (text-embedding-3-small size)
        - Metric: cosine (best for text similarity)
        - Cloud: AWS, Region: us-east-1 (free tier)
        """
        # Check if index already exists
        existing_indexes = [idx.name for idx in self.pc.list_indexes()]

        if self.index_name in existing_indexes:
            print(f"✅ Index '{self.index_name}' already exists")
            return self.pc.Index(self.index_name)

        print(f"🔨 Creating index '{self.index_name}'...")

        # Create index with serverless spec
        self.pc.create_index(
            name=self.index_name,
            dimension=PINECONE_DIMENSION,
            metric="cosine",  # Best for text embeddings
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"  # Free tier region
            )
        )

        # Wait for index to be ready
        print("⏳ Waiting for index to be ready...")
        while not self.pc.describe_index(self.index_name).status.ready:
            time.sleep(1)

        print(f"✅ Index '{self.index_name}' created successfully!")
        return self.pc.Index(self.index_name)

    def get_index(self):
        """Get existing index."""
        return self.pc.Index(self.index_name)

    def delete_index(self):
        """Delete the index (use carefully!)."""
        if self.index_name in [idx.name for idx in self.pc.list_indexes()]:
            self.pc.delete_index(self.index_name)
            print(f"🗑️  Index '{self.index_name}' deleted")
        else:
            print(f"❌ Index '{self.index_name}' does not exist")

    def get_index_stats(self):
        """Get index statistics."""
        index = self.get_index()
        stats = index.describe_index_stats()
        print(f"\n📊 Index Stats:")
        print(f"  Total vectors: {stats.total_vector_count}")
        print(f"  Dimension: {stats.dimension}")
        return stats
