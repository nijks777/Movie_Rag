"""
Check document sizes to decide chunking strategy.
"""

from src.config import NETFLIX_CSV, TV_SHOWS_CSV, IMDB_MOVIES_CSV
from src.utils.document_loader import MovieDocumentLoader
import tiktoken

def count_tokens(text: str) -> int:
    """Count tokens using OpenAI's tokenizer."""
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def main():
    print("📊 Analyzing Document Sizes...\n")

    # Load all documents
    documents = MovieDocumentLoader.load_all_datasets(
        netflix_path=NETFLIX_CSV,
        tv_shows_path=TV_SHOWS_CSV,
        imdb_path=IMDB_MOVIES_CSV
    )

    # Analyze sizes
    token_counts = [count_tokens(doc.page_content) for doc in documents[:100]]

    print(f"\n📏 Token Count Stats (first 100 docs):")
    print(f"  Min tokens: {min(token_counts)}")
    print(f"  Max tokens: {max(token_counts)}")
    print(f"  Avg tokens: {sum(token_counts) / len(token_counts):.1f}")

    print(f"\n💡 Analysis:")
    if max(token_counts) < 500:
        print("  ✅ Documents are SMALL (< 500 tokens)")
        print("  ✅ NO chunking needed - each doc is already optimal size!")
    else:
        print("  ⚠️  Some documents are LARGE (> 500 tokens)")
        print("  ⚠️  Chunking recommended for better retrieval")

if __name__ == "__main__":
    main()
