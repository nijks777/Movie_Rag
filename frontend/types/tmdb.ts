// TMDB API Type Definitions

export interface TMDBMovie {
  id: number;
  title: string;
  original_title: string;
  overview: string;
  poster_path: string | null;
  backdrop_path: string | null;
  release_date: string;
  vote_average: number;
  vote_count: number;
  popularity: number;
  genre_ids: number[];
  adult: boolean;
  video: boolean;
  original_language: string;
}

export interface TMDBTVShow {
  id: number;
  name: string;
  original_name: string;
  overview: string;
  poster_path: string | null;
  backdrop_path: string | null;
  first_air_date: string;
  vote_average: number;
  vote_count: number;
  popularity: number;
  genre_ids: number[];
  origin_country: string[];
  original_language: string;
}

export interface TMDBSearchResult {
  page: number;
  results: (TMDBMovie | TMDBTVShow)[];
  total_pages: number;
  total_results: number;
}

export interface TMDBCastMember {
  id: number;
  name: string;
  character: string;
  profile_path: string | null;
  order: number;
}

export interface TMDBCredits {
  id: number;
  cast: TMDBCastMember[];
  crew: any[];
}

export interface TMDBGenre {
  id: number;
  name: string;
}

export interface TMDBMovieDetails extends TMDBMovie {
  genres: TMDBGenre[];
  runtime: number;
  status: string;
  tagline: string;
  budget: number;
  revenue: number;
  production_companies: {
    id: number;
    name: string;
    logo_path: string | null;
  }[];
}

export interface TMDBTVDetails extends TMDBTVShow {
  genres: TMDBGenre[];
  number_of_seasons: number;
  number_of_episodes: number;
  status: string;
  tagline: string;
  created_by: {
    id: number;
    name: string;
    profile_path: string | null;
  }[];
}

export interface TMDBConfiguration {
  images: {
    base_url: string;
    secure_base_url: string;
    backdrop_sizes: string[];
    poster_sizes: string[];
    profile_sizes: string[];
  };
}

// Helper type to distinguish between movie and TV show
export type TMDBMediaType = 'movie' | 'tv';

export interface EnrichedMovieData {
  // Original backend data
  title: string;
  genre: string;
  rating: number;

  // TMDB enrichment
  tmdbId?: number;
  mediaType?: TMDBMediaType;
  posterPath?: string | null;
  backdropPath?: string | null;
  overview?: string;
  voteAverage?: number;
  releaseDate?: string;
  cast?: TMDBCastMember[];
  genres?: TMDBGenre[];
}
