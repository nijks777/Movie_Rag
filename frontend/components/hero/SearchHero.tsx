'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { buttonVariants, processingVariants } from '@/lib/utils/animations';

interface SearchHeroProps {
  query: string;
  loading: boolean;
  processingStep: string;
  onQueryChange: (query: string) => void;
  onSearch: () => void;
  onClear?: () => void;
  hasResults?: boolean;
}

export default function SearchHero({
  query,
  loading,
  processingStep,
  onQueryChange,
  onSearch,
  onClear,
  hasResults = false,
}: SearchHeroProps) {
  return (
    <div className="bg-cinema-dark border border-cinema-gray rounded-lg p-4 mb-6">
      <div className="flex gap-3">
        <motion.input
          type="text"
          value={query}
          onChange={(e) => onQueryChange(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSearch()}
          placeholder="Ask about movies or TV shows..."
          className="flex-1 bg-cinema-gray border border-cinema-gray rounded px-4 py-2 text-cinema-white placeholder-gray-500 focus:outline-none focus:border-cinema-gold transition-all"
          whileFocus={{ scale: 1.01 }}
          transition={{ duration: 0.2 }}
        />
        <motion.button
          onClick={onSearch}
          disabled={loading || !query.trim()}
          className="bg-cinema-gold text-cinema-black px-6 py-2 rounded font-semibold hover:bg-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          variants={buttonVariants}
          initial="rest"
          whileHover="hover"
          whileTap="tap"
        >
          {loading ? 'Searching...' : 'Search'}
        </motion.button>
        {hasResults && onClear && (
          <motion.button
            onClick={onClear}
            disabled={loading}
            className="bg-red-900 text-red-200 px-4 py-2 rounded font-semibold hover:bg-red-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            variants={buttonVariants}
            initial="rest"
            whileHover="hover"
            whileTap="tap"
            title="Clear results"
          >
            Clear
          </motion.button>
        )}
      </div>

      {/* Processing Indicator */}
      <AnimatePresence mode="wait">
        {loading && processingStep && (
          <motion.div
            key={processingStep}
            variants={processingVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
            className="mt-3 text-sm text-cinema-gold"
          >
            {processingStep}
          </motion.div>
        )}
      </AnimatePresence>

      <p className="text-xs text-gray-500 mt-2">
        Try: "action movies", "funny Indian shows", "Who won Oscar 2024?"
      </p>
    </div>
  );
}
