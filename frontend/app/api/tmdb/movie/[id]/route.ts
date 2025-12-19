import { NextRequest, NextResponse } from 'next/server';
import { getMovieDetails, getMovieCredits } from '@/lib/tmdb/client';

/**
 * TMDB Movie Details API Proxy
 * GET /api/tmdb/movie/[id]?include_credits=true
 *
 * Returns movie details and optionally credits (cast/crew)
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const movieId = parseInt(id, 10);

    if (isNaN(movieId)) {
      return NextResponse.json(
        { error: 'Invalid movie ID' },
        { status: 400 }
      );
    }

    const searchParams = request.nextUrl.searchParams;
    const includeCredits = searchParams.get('include_credits') === 'true';

    // Fetch movie details
    const details = await getMovieDetails(movieId);

    // Optionally fetch credits
    let credits = null;
    if (includeCredits) {
      credits = await getMovieCredits(movieId);
    }

    // Cache for 1 hour (movie details don't change often)
    return NextResponse.json(
      { details, credits },
      {
        headers: {
          'Cache-Control': 'public, s-maxage=3600, stale-while-revalidate=7200',
        },
      }
    );
  } catch (error) {
    console.error('TMDB movie details error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch movie details' },
      { status: 500 }
    );
  }
}
