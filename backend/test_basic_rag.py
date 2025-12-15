"""
Test Basic RAG Pipeline.
"""

from src.rag.basic_rag import BasicRAG
import json


def main():
    print("🎬 Testing Basic RAG Pipeline\n")
    print("=" * 80)

    # Initialize RAG
    rag = BasicRAG()

    # Test queries
    test_queries = [
        "What are some good action movies?",
        "Recommend me a comedy show from India",
        "What sci-fi series can I watch?",
        "Tell me about movies with high ratings"
    ]

    for i, question in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"Query {i}: {question}")
        print('='*80)

        # Get answer
        result = rag.query(question, k=3)

        # Display results
        print(f"\n💬 Answer:")
        print(result['answer'])

        print(f"\n📚 Sources ({result['num_sources']}):")
        for j, source in enumerate(result['sources'], 1):
            print(f"  {j}. {source['title']}")
            print(f"     Source: {source['source']} | Genre: {source['genre']} | Rating: {source['rating']}")

        print("\n")

    print("=" * 80)
    print("✅ Basic RAG test complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
