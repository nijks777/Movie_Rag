import { useQuery } from '@tanstack/react-query';
import type { MovieSuggestion } from '@/types/api';
import type { EnrichedMovieData, TMDBMovie, TMDBTVShow } from '@/types/tmdb';

interface TMDBSearchResponse {
  page: number;
  results: (TMDBMovie | TMDBTVShow)[];
  total_pages: number;
  total_results: number;
}

// Helper to determine if result is a movie or TV show
function isMovie(result: TMDBMovie | TMDBTVShow): result is TMDBMovie {
  return 'title' in result;
}

// Fetch TMDB data for a single movie title
async function fetchTMDBData(title: string, year?: string): Promise<EnrichedMovieData | null> {
  try {
    // Search TMDB using our proxy API
    const searchParams = new URLSearchParams({ q: title });
    const response = await fetch(`/api/tmdb/search?${searchParams}`);

    if (!response.ok) {
      console.error(`TMDB search failed for "${title}"`);
      return null;
    }

    const data: TMDBSearchResponse = await response.json();

    if (!data.results || data.results.length === 0) {
      return null;
    }

    // Get first result (best match)
    const result = data.results[0];

    // Optionally fetch credits (cast) - for now we'll skip to reduce API calls
    // In Phase 5 we can add this with a separate endpoint

    if (isMovie(result)) {
      return {
        title: result.title,
        genre: '', // Will be populated from backend
        rating: 0, // Will be populated from backend
        tmdbId: result.id,
        mediaType: 'movie',
        posterPath: result.poster_path,
        backdropPath: result.backdrop_path,
        overview: result.overview,
        voteAverage: result.vote_average,
        releaseDate: result.release_date,
      };
    } else {
      return {
        title: result.name,
        genre: '', // Will be populated from backend
        rating: 0, // Will be populated from backend
        tmdbId: result.id,
        mediaType: 'tv',
        posterPath: result.poster_path,
        backdropPath: result.backdrop_path,
        overview: result.overview,
        voteAverage: result.vote_average,
        releaseDate: result.first_air_date,
      };
    }
  } catch (error) {
    console.error(`Error fetching TMDB data for "${title}":`, error);
    return null;
  }
}

// Batch fetch TMDB data for multiple movies
async function batchFetchMovieData(suggestions: MovieSuggestion[]): Promise<EnrichedMovieData[]> {
  // Fetch all movies in parallel (with a small batch size to respect rate limits)
  const batchSize = 5;
  const enrichedData: EnrichedMovieData[] = [];

  for (let i = 0; i < suggestions.length; i += batchSize) {
    const batch = suggestions.slice(i, i + batchSize);
    const promises = batch.map(movie => fetchTMDBData(movie.title, movie.year));
    const results = await Promise.all(promises);

    // Merge backend data with TMDB data
    batch.forEach((movie, index) => {
      const tmdbData = results[index];
      enrichedData.push({
        // Original backend data
        title: movie.title,
        genre: movie.genre,
        rating: parseFloat(movie.rating) || 0,

        // TMDB enrichment (if available)
        ...(tmdbData && {
          tmdbId: tmdbData.tmdbId,
          mediaType: tmdbData.mediaType,
          posterPath: tmdbData.posterPath,
          backdropPath: tmdbData.backdropPath,
          overview: tmdbData.overview,
          voteAverage: tmdbData.voteAverage,
          releaseDate: tmdbData.releaseDate,
        }),
      });
    });

    // Small delay between batches to be nice to the API
    if (i + batchSize < suggestions.length) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  return enrichedData;
}

/**
 * Hook to fetch and enrich movie data with TMDB information
 * @param suggestions - Movie suggestions from backend
 * @returns Enriched movie data with TMDB posters, backdrops, etc.
 */
export function useMovieData(suggestions: MovieSuggestion[] | undefined) {
  return useQuery({
    queryKey: ['movies', suggestions?.map(s => s.title).join(',')],
    queryFn: () => batchFetchMovieData(suggestions || []),
    enabled: !!suggestions && suggestions.length > 0,
    staleTime: 1000 * 60 * 15, // 15 minutes
    gcTime: 1000 * 60 * 60, // 1 hour (formerly cacheTime)
  });
}
