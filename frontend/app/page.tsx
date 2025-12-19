'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Header from '@/components/layout/Header';
import EmptyState from '@/components/layout/EmptyState';
import SearchHero from '@/components/hero/SearchHero';
import AnswerCard from '@/components/results/AnswerCard';
import SourcesAccordion from '@/components/results/SourcesAccordion';
import MovieGrid from '@/components/movie/MovieGrid';
import type { CompareResponse } from '@/types/api';
import { pageVariants, fadeInUp } from '@/lib/utils/animations';
import ParticleBackground from '@/components/ui/ParticleBackground';

const STORAGE_KEY = 'movie-rag-search';

export default function Home() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [processingStep, setProcessingStep] = useState('');
  const [result, setResult] = useState<CompareResponse | null>(null);
  const [error, setError] = useState('');

  // Load saved search from localStorage on mount
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const { query: savedQuery, result: savedResult } = JSON.parse(saved);
        setQuery(savedQuery);
        setResult(savedResult);
      }
    } catch (err) {
      console.error('Failed to load saved search:', err);
    }
  }, []);

  // Save search to localStorage whenever query or result changes
  useEffect(() => {
    if (result) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ query, result }));
      } catch (err) {
        console.error('Failed to save search:', err);
      }
    }
  }, [query, result]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      setProcessingStep('🔍 Searching vector database...');
      await new Promise(resolve => setTimeout(resolve, 300));

      setProcessingStep('🌐 Fetching web results...');
      await new Promise(resolve => setTimeout(resolve, 300));

      setProcessingStep('🤖 Generating answer...');
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/search/compare`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query, k: 5 }),
      });

      if (!response.ok) {
        throw new Error('Search failed');
      }

      const data = await response.json();
      console.log('Search result:', data);
      setResult(data);
      setProcessingStep('');
    } catch (err) {
      console.error('Search error:', err);
      setError('Failed to search. Make sure the backend is running on localhost:8000');
      setProcessingStep('');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setQuery('');
    setResult(null);
    setError('');
    localStorage.removeItem(STORAGE_KEY);
  };

  return (
    <motion.div
      className="min-h-screen bg-cinema-black text-cinema-light relative z-10"
      initial="hidden"
      animate="visible"
      variants={pageVariants}
    >
      <ParticleBackground />
      <Header />

      <main className="max-w-6xl mx-auto px-4 py-6 relative">
        <motion.div variants={fadeInUp}>
          <SearchHero
            query={query}
            loading={loading}
            processingStep={processingStep}
            onQueryChange={setQuery}
            onSearch={handleSearch}
            onClear={handleClear}
            hasResults={!!result}
          />
        </motion.div>

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-900 border border-red-700 text-red-200 rounded-lg p-3 mb-6 text-sm"
          >
            {error}
          </motion.div>
        )}

        {/* Results */}
        {result && (
          <motion.div
            initial="hidden"
            animate="visible"
            transition={{ staggerChildren: 0.15 }}
            className="space-y-4"
          >
            <motion.div variants={fadeInUp}>
              <AnswerCard answer={result.combined_answer} />
            </motion.div>
            <motion.div variants={fadeInUp}>
              <SourcesAccordion ragResult={result.rag_result} webResult={result.web_result} />
            </motion.div>
            <motion.div variants={fadeInUp}>
              <MovieGrid suggestions={result.suggestions || []} />
            </motion.div>
          </motion.div>
        )}

        {/* Empty State */}
        {!result && !loading && !error && (
          <motion.div variants={fadeInUp}>
            <EmptyState />
          </motion.div>
        )}
      </main>
    </motion.div>
  );
}
