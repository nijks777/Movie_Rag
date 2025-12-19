// Shared API types used across the application

export interface Source {
  title: string;
  source: string;
}

export interface SearchResult {
  answer: string;
  sources: Source[];
  num_sources?: number;
}

export interface MovieSuggestion {
  title: string;
  genre: string;
  rating: string;
  source: string;
  year: string;
}

export interface CompareResponse {
  query: string;
  rag_result: SearchResult;
  web_result: SearchResult;
  combined_answer: string;
  suggestions?: MovieSuggestion[];
}
