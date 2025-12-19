"""
Document Loader for CSV datasets.
Loads movie/TV show data and converts to LangChain Documents.
"""

import pandas as pd
from pathlib import Path
from typing import List
from langchain_core.documents import Document


class MovieDocumentLoader:
    """
    Loads movie/TV show datasets from CSV files.

    Best Practices:
    1. Combine multiple columns for rich context
    2. Add metadata for filtering and tracing
    3. Handle missing values gracefully
    4. Normalize text (strip whitespace, handle nulls)
    """

    def __init__(self, csv_path: Path):
        """
        Initialize the document loader.

        Args:
            csv_path: Path to the CSV file
        """
        self.csv_path = csv_path

    def load_netflix_data(self) -> List[Document]:
        """
        Load Netflix movies and TV shows dataset.

        Returns:
            List of LangChain Document objects
        """
        df = pd.read_csv(self.csv_path)

        # Handle missing values
        df = df.fillna("")

        documents = []

        for idx, row in df.iterrows():
            # Combine multiple columns for rich context
            # This gives the LLM more information to retrieve from
            content = f"""
Title: {row['title']}
Type: {row['type']}
Description: {row['description']}
Director: {row['director']}
Cast: {row['cast']}
Country: {row['country']}
Listed In: {row['listed_in']}
            """.strip()

            # Metadata helps with filtering and provides context
            metadata = {
                "source": "netflix",
                "show_id": row['show_id'],
                "title": row['title'],
                "type": row['type'],
                "release_year": str(row['release_year']),
                "rating": row['rating'],
                "duration": row['duration'],
                "genre": row['listed_in'],
                "country": row['country'],
            }

            documents.append(Document(page_content=content, metadata=metadata))

        return documents

    def load_tv_shows_data(self) -> List[Document]:
        """
        Load top-rated TV shows dataset.

        Returns:
            List of LangChain Document objects
        """
        df = pd.read_csv(self.csv_path)

        # Handle missing values
        df = df.fillna("")

        documents = []

        for idx, row in df.iterrows():
            # Combine relevant columns
            content = f"""
Title: {row['title']}
Original Title: {row['original_title']}
Overview: {row['overview']}
Genre: {row['genre']}
Country: {row['country_origin']}
Language: {row['original_language']}
            """.strip()

            # Rich metadata for filtering
            metadata = {
                "source": "tv_shows",
                "show_id": str(row['id']),
                "title": row['title'],
                "premiere_date": str(row['premiere_date']),
                "popularity": str(row['popularity']),
                "genre": row['genre'],
                "country": row['country_origin'],
                "language": row['original_language'],
                "rating": str(row['rating']),
                "votes": str(row['votes']),
            }

            documents.append(Document(page_content=content, metadata=metadata))

        return documents

    def load_imdb_movies_data(self) -> List[Document]:
        """
        Load IMDB Indian movies dataset.

        Returns:
            List of LangChain Document objects
        """
        df = pd.read_csv(self.csv_path)

        # Handle missing values
        df = df.fillna("")

        documents = []

        for idx, row in df.iterrows():
            # Combine relevant columns
            content = f"""
Title: {row['Name']}
Year: {row['Year']}
Duration: {row['Duration']} minutes
Genre: {row['Genre']}
Rating: {row['Rating']}
Director: {row['Director']}
Cast: {row['Actor 1']}, {row['Actor 2']}, {row['Actor 3']}
            """.strip()

            # Rich metadata for filtering
            metadata = {
                "source": "imdb_indian",
                "title": row['Name'],
                "year": str(row['Year']),
                "duration": str(row['Duration']),
                "genre": row['Genre'],
                "rating": str(row['Rating']),
                "votes": str(row['Votes']),
                "director": row['Director'],
            }

            documents.append(Document(page_content=content, metadata=metadata))

        return documents

    def load_new_imdb_data(self) -> List[Document]:
        """
        Load the new IMDB movies dataset (IMBD.csv).

        Returns:
            List of LangChain Document objects
        """
        df = pd.read_csv(self.csv_path)

        # Handle missing values
        df = df.fillna("")

        documents = []

        for idx, row in df.iterrows():
            # Combine relevant columns
            content = f"""
Title: {row['title']}
Year: {row['year']}
Duration: {row['duration']}
Genre: {row['genre']}
Rating: {row['rating']}
Description: {row['description']}
Stars: {row['stars']}
Votes: {row['votes']}
            """.strip()

            # Rich metadata for filtering
            metadata = {
                "source": "new_imdb", # Differentiate from existing IMDB
                "title": row['title'],
                "year": str(row['year']),
                "duration": row['duration'],
                "genre": row['genre'],
                "rating": str(row['rating']),
                "votes": row['votes'],
                "description": row['description'],
                "stars": row['stars'],
            }

            documents.append(Document(page_content=content, metadata=metadata))

        return documents

    @staticmethod
    def load_all_datasets(netflix_path: Path, tv_shows_path: Path, imdb_path: Path) -> List[Document]:
        """
        Load all datasets and combine them.

        Args:
            netflix_path: Path to Netflix CSV
            tv_shows_path: Path to TV shows CSV
            imdb_path: Path to IMDB movies CSV

        Returns:
            Combined list of all documents
        """
        all_documents = []

        # Load Netflix data
        netflix_loader = MovieDocumentLoader(netflix_path)
        netflix_docs = netflix_loader.load_netflix_data()
        all_documents.extend(netflix_docs)
        print(f"✅ Loaded {len(netflix_docs)} Netflix documents")

        # Load TV shows data
        tv_loader = MovieDocumentLoader(tv_shows_path)
        tv_docs = tv_loader.load_tv_shows_data()
        all_documents.extend(tv_docs)
        print(f"✅ Loaded {len(tv_docs)} TV show documents")

        # Load IMDB Indian movies data
        imdb_loader = MovieDocumentLoader(imdb_path)
        imdb_docs = imdb_loader.load_imdb_movies_data()
        all_documents.extend(imdb_docs)
        print(f"✅ Loaded {len(imdb_docs)} IMDB Indian movie documents")

        print(f"📊 Total documents: {len(all_documents)}")

        return all_documents
