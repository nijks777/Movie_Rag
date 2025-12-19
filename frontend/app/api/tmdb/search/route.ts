import { NextRequest, NextResponse } from 'next/server';
import { searchMulti } from '@/lib/tmdb/client';

/**
 * TMDB Search API Proxy
 * GET /api/tmdb/search?q=movie+title
 *
 * This proxy:
 * 1. Hides TMDB API key from client
 * 2. Enables server-side caching
 * 3. Handles rate limiting
 */
export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams;
    const query = searchParams.get('q');

    if (!query) {
      return NextResponse.json(
        { error: 'Query parameter "q" is required' },
        { status: 400 }
      );
    }

    // Search TMDB
    const results = await searchMulti(query);

    // Cache for 15 minutes
    return NextResponse.json(results, {
      headers: {
        'Cache-Control': 'public, s-maxage=900, stale-while-revalidate=1800',
      },
    });
  } catch (error) {
    console.error('TMDB search error:', error);
    return NextResponse.json(
      { error: 'Failed to search TMDB' },
      { status: 500 }
    );
  }
}
