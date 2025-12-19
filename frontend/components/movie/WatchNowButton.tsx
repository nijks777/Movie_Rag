'use client';

import { motion } from 'framer-motion';
import { generateSearchLink } from '@/types/streaming';

interface WatchNowButtonProps {
  title: string;
  year?: string;
}

export default function WatchNowButton({ title, year }: WatchNowButtonProps) {
  const searchLink = generateSearchLink(title, year);

  return (
    <motion.a
      href={searchLink}
      target="_blank"
      rel="noopener noreferrer"
      className="mt-2 w-full bg-cinema-gold text-cinema-black px-3 py-1.5 rounded text-xs font-semibold hover:bg-yellow-500 transition-colors flex items-center justify-center gap-1.5"
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <span>🔍</span>
      <span>Find Where to Watch</span>
    </motion.a>
  );
}
