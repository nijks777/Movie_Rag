import os
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import PodSpec

from src.config import (
    PINECONE_API_KEY,
    OPENAI_API_KEY,
    EMBEDDING_MODEL,
    PINECONE_INDEX_NAME # Use the index name from config
)
from src.utils.document_loader import MovieDocumentLoader

console = Console()

def ingest_imdb_data(file_path: Path):
    """
    Loads IMBD.csv data, generates embeddings, and ingests into Pinecone.
    """
    console.print(f"🚀 [bold green]Starting ingestion of IMBD.csv data from {file_path}...[/bold green]")

    # Initialize OpenAI Embeddings
    console.print("🔄 [yellow]Initializing OpenAI Embeddings...[/yellow]")
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY
    )
    console.print("✅ [green]Embeddings initialized.[/green]")

    # Load data using the new loader
    console.print(f"📚 [yellow]Loading documents from {file_path}...[/yellow]")
    loader = MovieDocumentLoader(file_path)
    documents = loader.load_new_imdb_data()
    console.print(f"✅ [green]Loaded {len(documents)} documents.[/green]")

    # Initialize Pinecone Vector Store
    console.print("🌲 [yellow]Initializing Pinecone Vector Store...[/yellow]")
    if PINECONE_API_KEY is None:
        console.print("❌ [bold red]Pinecone API Key or Environment not set. Skipping Pinecone initialization.[/bold red]")
        console.print("Please set PINECONE_API_KEY and PINECONE_ENVIRONMENT in your .env file.")
        return

    # Ensure index exists or create it
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task("[yellow]Checking/Creating Pinecone index...", total=None)
        
        # This will create the index if it doesn't exist
        # If using serverless, spec is not needed. If using pod, it might be.
        # Assuming serverless for simplicity or handling in the PineconeVectorStore init
        vector_store = PineconeVectorStore.from_documents(
            documents,
            index_name=PINECONE_INDEX_NAME,
            embedding=embeddings
        )
        progress.update(task, description="[green]Pinecone index ready.[/green]")
    
    console.print(f"✅ [green]Data ingested into Pinecone index: {PINECONE_INDEX_NAME}[/green]")
    console.print("✨ [bold green]IMBD.csv data ingestion complete![/bold green]")

if __name__ == "__main__":
    # Ensure environment variables are loaded
    from dotenv import load_dotenv
    load_dotenv()

    # Use absolute path from current directory
    IMDB_CSV_PATH = Path(__file__).parent / "data" / "IMBD.csv"

    if not IMDB_CSV_PATH.exists():
        console.print(f"❌ [bold red]File not found: {IMDB_CSV_PATH}[/bold red]")
        exit(1)

    ingest_imdb_data(IMDB_CSV_PATH)
