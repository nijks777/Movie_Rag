"""
Upload all movie/TV documents to Pinecone.

This will:
1. Load all 15,446 documents
2. Generate embeddings via OpenAI
3. Upload to Pinecone
4. Cost: ~$0.03
"""

from src.config import NETFLIX_CSV, TV_SHOWS_CSV, IMDB_MOVIES_CSV
from src.utils.document_loader import MovieDocumentLoader
from src.rag.embeddings import DocumentEmbedder
from src.rag.vector_store import PineconeVectorStore


def main():
    print("🎬 Movie RAG - Document Upload Pipeline\n")
    print("=" * 60)

    # Step 1: Load documents
    print("\n📚 Step 1: Loading documents...")
    documents = MovieDocumentLoader.load_all_datasets(
        netflix_path=NETFLIX_CSV,
        tv_shows_path=TV_SHOWS_CSV,
        imdb_path=IMDB_MOVIES_CSV
    )

    # Step 2: Embed and upload
    print("\n🔮 Step 2: Generating embeddings and uploading to Pinecone...")
    embedder = DocumentEmbedder()
    vector_store = embedder.embed_and_upload(documents, batch_size=100)

    # Step 3: Verify upload
    print("\n📊 Step 3: Verifying upload...")
    vs = PineconeVectorStore()
    vs.get_index_stats()

    print("\n" + "=" * 60)
    print("✅ Upload complete! Your RAG system is ready!")
    print("=" * 60)


if __name__ == "__main__":
    main()
