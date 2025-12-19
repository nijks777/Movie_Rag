'use client';

import { motion } from 'framer-motion';
import Image from 'next/image';
import type { EnrichedMovieData } from '@/types/tmdb';
import { getPosterUrl, getBackdropUrl } from '@/lib/tmdb/client';
import { movieCardVariants, backdropVariants, posterVariants } from '@/lib/utils/animations';
import WatchNowButton from './WatchNowButton';

interface MovieCardProps {
  movie: EnrichedMovieData;
}

export default function MovieCard({ movie }: MovieCardProps) {
  const posterUrl = getPosterUrl(movie.posterPath || null, 'w342');
  const backdropUrl = getBackdropUrl(movie.backdropPath || null, 'w780');

  return (
    <motion.div
      className="relative bg-cinema-gray border border-cinema-gray rounded-lg overflow-hidden hover:border-cinema-gold transition-colors group cursor-pointer"
      variants={movieCardVariants}
      whileHover="hover"
      whileTap="tap"
    >
      {/* Backdrop blur effect (appears on hover) */}
      {backdropUrl && (
        <motion.div
          className="absolute inset-0 opacity-0"
          initial="hidden"
          whileHover="visible"
          variants={backdropVariants}
        >
          <Image
            src={backdropUrl}
            alt=""
            fill
            className="object-cover blur-xl scale-110"
            sizes="(max-width: 768px) 50vw, 20vw"
            loading="lazy"
          />
        </motion.div>
      )}

      {/* Content */}
      <div className="relative p-3">
        {/* Poster */}
        {posterUrl ? (
          <motion.div
            className="relative w-full aspect-2/3 mb-2 rounded overflow-hidden bg-cinema-dark"
            variants={posterVariants}
          >
            <Image
              src={posterUrl}
              alt={movie.title}
              fill
              className="object-cover"
              sizes="(max-width: 768px) 50vw, 20vw"
              loading="eager"
              priority={false}
              placeholder="blur"
              blurDataURL="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjYwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjYwMCIgZmlsbD0iIzFhMWExYSIvPjwvc3ZnPg=="
            />
          </motion.div>
        ) : (
          // Fallback for missing poster
          <div className="relative w-full aspect-2/3 mb-2 rounded overflow-hidden bg-cinema-dark flex items-center justify-center">
            <div className="text-4xl">🎬</div>
          </div>
        )}

        {/* Movie Info */}
        <div>
          <h3 className="font-semibold text-cinema-white mb-1 text-xs leading-tight line-clamp-2">
            {movie.title}
          </h3>

          <div className="space-y-0.5 text-xs">
            {/* Genre */}
            {movie.genre && (
              <p className="text-gray-400 truncate">{movie.genre}</p>
            )}

            {/* Rating - prefer TMDB vote_average, fallback to backend rating */}
            <div className="flex items-center gap-1">
              <span className="text-cinema-gold">⭐</span>
              <span className="text-cinema-gold font-medium">
                {movie.voteAverage
                  ? movie.voteAverage.toFixed(1)
                  : movie.rating?.toFixed(1) || 'N/A'}
              </span>
              {movie.voteAverage && (
                <span className="text-gray-500 text-[10px]">/10</span>
              )}
            </div>

            {/* Release year */}
            {movie.releaseDate && (
              <p className="text-gray-500 text-[10px]">
                {new Date(movie.releaseDate).getFullYear()}
              </p>
            )}
          </div>

          {/* Watch Now Button */}
          <WatchNowButton
            title={movie.title}
            year={movie.releaseDate ? new Date(movie.releaseDate).getFullYear().toString() : undefined}
          />
        </div>
      </div>
    </motion.div>
  );
}
