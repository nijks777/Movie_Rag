"""
Test Enhanced RAG with different query strategies.
Compare: Basic vs HyDE vs Multi-Query vs Expansion
"""

from src.rag.enhanced_rag import EnhancedRAG


def test_strategy(rag, question, strategy):
    """Test a single strategy."""
    print("\n" + "="*80)
    print(f"STRATEGY: {strategy.upper()}")
    print("="*80)

    result = rag.query_enhanced(question, strategy=strategy, k=3)

    print(f"\n💬 Answer:")
    print(result['answer'])

    print(f"\n📚 Sources ({result['num_sources']}):")
    for i, source in enumerate(result['sources'], 1):
        print(f"  {i}. {source['title']}")
        print(f"     {source['genre']} | {source['rating']}")


def main():
    print("🎬 Testing Enhanced RAG Strategies\n")

    # Initialize enhanced RAG
    rag = EnhancedRAG()

    # Test query
    question = "funny Indian shows"

    print(f"Test Question: '{question}'")
    print("\n" + "="*80)

    # Test all strategies
    strategies = ["basic", "hyde", "multi_query", "expansion"]

    for strategy in strategies:
        test_strategy(rag, question, strategy)

    print("\n" + "="*80)
    print("✅ Enhanced RAG test complete!")
    print("="*80)


if __name__ == "__main__":
    main()
