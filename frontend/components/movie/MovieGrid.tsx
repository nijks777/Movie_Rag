'use client';

import { motion } from 'framer-motion';
import type { MovieSuggestion } from '@/types/api';
import type { EnrichedMovieData } from '@/types/tmdb';
import { useMovieData } from '@/hooks/useMovieData';
import MovieCard from './MovieCard';

interface MovieGridProps {
  suggestions: MovieSuggestion[];
}

export default function MovieGrid({ suggestions }: MovieGridProps) {
  const { data: enrichedMovies, isLoading } = useMovieData(suggestions);

  if (!suggestions || suggestions.length === 0) {
    return null;
  }

  // Convert basic suggestions to EnrichedMovieData format
  const basicMovies: EnrichedMovieData[] = suggestions.map(movie => ({
    title: movie.title,
    genre: movie.genre,
    rating: parseFloat(movie.rating) || 0,
  }));

  // Use enriched data if available, otherwise use basic data
  const displayMovies = enrichedMovies || basicMovies;

  return (
    <div className="bg-cinema-dark border border-cinema-gray rounded-lg p-4">
      <h2 className="text-sm font-bold text-cinema-gold mb-3">
        🍿 You Might Also Like
        {isLoading && <span className="text-xs text-gray-500 ml-2">(Loading images...)</span>}
      </h2>

      <motion.div
        className="grid grid-cols-2 md:grid-cols-5 gap-3"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        {displayMovies.map((movie, idx) => (
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: idx * 0.05 }}
          >
            <MovieCard movie={movie} />
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
