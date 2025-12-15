"""
Test semantic search retrieval from Pinecone.
"""

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from src.config import OPENAI_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL


def main():
    print("🔍 Testing Semantic Search...\n")

    # Initialize embeddings and vector store
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )

    # Test queries
    queries = [
        "action movies with high ratings",
        "comedy shows from India",
        "sci-fi TV series"
    ]

    for query in queries:
        print(f"📝 Query: '{query}'")
        print("-" * 60)

        # Semantic search
        results = vector_store.similarity_search(query, k=3)

        for i, doc in enumerate(results, 1):
            print(f"\n{i}. {doc.metadata.get('title', 'N/A')}")
            print(f"   Source: {doc.metadata.get('source', 'N/A')}")
            print(f"   Genre: {doc.metadata.get('genre', 'N/A')}")
            print(f"   Rating: {doc.metadata.get('rating', 'N/A')}")

        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
