"""
Test script to verify document loader works correctly.
"""

from src.config import NETFLIX_CSV, TV_SHOWS_CSV, IMDB_MOVIES_CSV
from src.utils.document_loader import MovieDocumentLoader


def main():
    print("🚀 Testing Document Loader...\n")

    # Load all documents
    documents = MovieDocumentLoader.load_all_datasets(
        netflix_path=NETFLIX_CSV,
        tv_shows_path=TV_SHOWS_CSV,
        imdb_path=IMDB_MOVIES_CSV
    )

    print(f"\n📄 Sample Document:")
    print("=" * 60)
    print(documents[0].page_content)
    print("\n🏷️  Metadata:")
    print(documents[0].metadata)
    print("=" * 60)

    print(f"\n✅ Document loader test passed!")


if __name__ == "__main__":
    main()
