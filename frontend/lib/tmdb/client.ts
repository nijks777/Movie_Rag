import type {
  TMDBSearchResult,
  TMDBMovieDetails,
  TMDBTVDetails,
  TMDBCredits,
  TMDBConfiguration,
} from '@/types/tmdb';

const TMDB_API_KEY = process.env.NEXT_PUBLIC_TMDB_API_KEY;
const TMDB_BASE_URL = 'https://api.themoviedb.org/3';
export const TMDB_IMAGE_BASE = 'https://image.tmdb.org/t/p';

// Simple in-memory cache with TTL
interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

class TMDBCache {
  private cache = new Map<string, CacheEntry<any>>();
  private ttl = 15 * 60 * 1000; // 15 minutes

  get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;

    const now = Date.now();
    if (now - entry.timestamp > this.ttl) {
      this.cache.delete(key);
      return null;
    }

    return entry.data as T;
  }

  set<T>(key: string, data: T): void {
    this.cache.set(key, {
      data,
      timestamp: Date.now(),
    });
  }

  clear(): void {
    this.cache.clear();
  }
}

const cache = new TMDBCache();

// Helper function to build TMDB API URLs
function buildUrl(endpoint: string, params: Record<string, string> = {}): string {
  const url = new URL(`${TMDB_BASE_URL}${endpoint}`);
  url.searchParams.append('api_key', TMDB_API_KEY || '');

  Object.entries(params).forEach(([key, value]) => {
    url.searchParams.append(key, value);
  });

  return url.toString();
}

// Generic fetch function with error handling
async function tmdbFetch<T>(endpoint: string, params: Record<string, string> = {}): Promise<T> {
  if (!TMDB_API_KEY) {
    throw new Error('TMDB API key is not configured');
  }

  const cacheKey = `${endpoint}:${JSON.stringify(params)}`;
  const cached = cache.get<T>(cacheKey);
  if (cached) {
    return cached;
  }

  const url = buildUrl(endpoint, params);

  try {
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`TMDB API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    cache.set(cacheKey, data);

    return data as T;
  } catch (error) {
    console.error('TMDB fetch error:', error);
    throw error;
  }
}

// Search for movies and TV shows by title
export async function searchMulti(query: string, page: number = 1): Promise<TMDBSearchResult> {
  return tmdbFetch<TMDBSearchResult>('/search/multi', {
    query,
    page: page.toString(),
    include_adult: 'false',
  });
}

// Search for movies only
export async function searchMovies(query: string, page: number = 1): Promise<TMDBSearchResult> {
  return tmdbFetch<TMDBSearchResult>('/search/movie', {
    query,
    page: page.toString(),
    include_adult: 'false',
  });
}

// Search for TV shows only
export async function searchTVShows(query: string, page: number = 1): Promise<TMDBSearchResult> {
  return tmdbFetch<TMDBSearchResult>('/search/tv', {
    query,
    page: page.toString(),
    include_adult: 'false',
  });
}

// Get movie details by ID
export async function getMovieDetails(movieId: number): Promise<TMDBMovieDetails> {
  return tmdbFetch<TMDBMovieDetails>(`/movie/${movieId}`);
}

// Get TV show details by ID
export async function getTVDetails(tvId: number): Promise<TMDBTVDetails> {
  return tmdbFetch<TMDBTVDetails>(`/tv/${tvId}`);
}

// Get movie credits (cast & crew)
export async function getMovieCredits(movieId: number): Promise<TMDBCredits> {
  return tmdbFetch<TMDBCredits>(`/movie/${movieId}/credits`);
}

// Get TV show credits
export async function getTVCredits(tvId: number): Promise<TMDBCredits> {
  return tmdbFetch<TMDBCredits>(`/tv/${tvId}/credits`);
}

// Get TMDB configuration (for image URLs)
export async function getConfiguration(): Promise<TMDBConfiguration> {
  return tmdbFetch<TMDBConfiguration>('/configuration');
}

// Helper: Build poster URL
export function getPosterUrl(posterPath: string | null, size: 'w185' | 'w342' | 'w500' | 'original' = 'w500'): string | null {
  if (!posterPath) return null;
  return `${TMDB_IMAGE_BASE}/${size}${posterPath}`;
}

// Helper: Build backdrop URL
export function getBackdropUrl(backdropPath: string | null, size: 'w780' | 'w1280' | 'original' = 'w1280'): string | null {
  if (!backdropPath) return null;
  return `${TMDB_IMAGE_BASE}/${size}${backdropPath}`;
}

// Helper: Build profile URL for cast photos
export function getProfileUrl(profilePath: string | null, size: 'w185' | 'h632' | 'original' = 'w185'): string | null {
  if (!profilePath) return null;
  return `${TMDB_IMAGE_BASE}/${size}${profilePath}`;
}

// Batch search for multiple titles (used to enrich backend suggestions)
export async function batchSearchTitles(titles: string[]): Promise<Map<string, TMDBSearchResult>> {
  const results = new Map<string, TMDBSearchResult>();

  // Process in batches of 5 to avoid rate limiting
  const batchSize = 5;
  for (let i = 0; i < titles.length; i += batchSize) {
    const batch = titles.slice(i, i + batchSize);
    const promises = batch.map(title =>
      searchMulti(title).catch(error => {
        console.error(`Failed to search for "${title}":`, error);
        return null;
      })
    );

    const batchResults = await Promise.all(promises);
    batch.forEach((title, index) => {
      const result = batchResults[index];
      if (result) {
        results.set(title, result);
      }
    });

    // Small delay between batches to respect rate limits
    if (i + batchSize < titles.length) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }

  return results;
}

// Clear cache (useful for testing)
export function clearCache(): void {
  cache.clear();
}
