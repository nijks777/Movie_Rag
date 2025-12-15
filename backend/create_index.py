"""
Script to create Pinecone index.
Run this once to set up the vector database.
"""

from src.rag.vector_store import PineconeVectorStore


def main():
    print("🚀 Setting up Pinecone Vector Database...\n")

    # Initialize vector store
    vector_store = PineconeVectorStore()

    # Create index
    index = vector_store.create_index()

    # Show stats
    vector_store.get_index_stats()

    print("\n✅ Pinecone setup complete!")


if __name__ == "__main__":
    main()
