"""
Test Corrective RAG Pipeline.

Test Cases:
1. Relevant query (should use vector DB)
2. Irrelevant query (should trigger web search)
"""

from src.rag.corrective_rag import CorrectiveRAG


def print_result(result):
    """Pretty print result."""
    print(f"\n💬 ANSWER:")
    print(result['answer'])

    print(f"\n📊 METADATA:")
    metadata = result['metadata']
    print(f"   Strategy: {metadata['strategy']}")
    print(f"   Relevance Score: {metadata['relevance_score']}/10")
    print(f"   Explanation: {metadata['score_explanation']}")
    print(f"   Used Web Search: {'YES' if metadata['used_web_search'] else 'NO'}")
    print(f"   Answer Grounded: {'✅ YES' if metadata['is_grounded'] else '❌ NO'}")
    print(f"   Verification: {metadata['verification_feedback']}")

    print(f"\n📚 SOURCES ({metadata['num_sources']}):")
    for i, source in enumerate(result['sources'], 1):
        print(f"   {i}. {source['title']} ({source['source']})")


def main():
    print("🎬 Testing Corrective RAG Pipeline\n")
    print("="*80)

    # Initialize Corrective RAG
    rag = CorrectiveRAG()

    # Test Case 1: Relevant query (in our database)
    print("\n" + "="*80)
    print("TEST CASE 1: Relevant Query (Should Use Vector DB)")
    print("="*80)

    question1 = "What are some action movies with high ratings?"
    result1 = rag.query_corrective(
        question=question1,
        strategy="multi_query",
        k=3,
        enable_web_fallback=True,
        enable_verification=True
    )

    print_result(result1)

    # Test Case 2: Irrelevant query (NOT in our database)
    print("\n\n" + "="*80)
    print("TEST CASE 2: Irrelevant Query (Should Trigger Web Search)")
    print("="*80)

    question2 = "Who won the Oscar for Best Picture in 2024?"
    result2 = rag.query_corrective(
        question=question2,
        strategy="basic",
        k=3,
        enable_web_fallback=True,
        enable_verification=True
    )

    print_result(result2)

    print("\n\n" + "="*80)
    print("✅ Corrective RAG test complete!")
    print("="*80)


if __name__ == "__main__":
    main()
