'use client';

import { motion } from 'framer-motion';

interface Source {
  title: string;
  source: string;
}

interface SearchResult {
  answer: string;
  sources: Source[];
  num_sources?: number;
}

interface SourcesAccordionProps {
  ragResult: SearchResult;
  webResult: SearchResult;
}

export default function SourcesAccordion({ ragResult, webResult }: SourcesAccordionProps) {
  return (
    <motion.details
      className="bg-cinema-dark border border-cinema-gray rounded-lg p-4"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.15 }}
    >
      <summary className="cursor-pointer font-semibold text-cinema-gold text-sm">
        📚 View Sources ({ragResult.num_sources || 0} Database + {webResult.num_sources || 0} Web)
      </summary>
      <div className="mt-3 grid md:grid-cols-2 gap-4">
        {/* Database Sources */}
        <div>
          <h4 className="text-xs font-bold text-cinema-light mb-2">Database Results:</h4>
          <ul className="space-y-1">
            {ragResult.sources.slice(0, 3).map((source, idx) => (
              <li key={idx} className="text-xs text-gray-400">
                • {source.title}
              </li>
            ))}
          </ul>
        </div>

        {/* Web Sources */}
        {(webResult.num_sources || 0) > 0 && (
          <div>
            <h4 className="text-xs font-bold text-cinema-light mb-2">Web Results:</h4>
            <ul className="space-y-1">
              {webResult.sources.map((source, idx) => (
                <li key={idx} className="text-xs text-gray-400">
                  • {source.title}{' '}
                  {source.source.startsWith('http') && (
                    <a
                      href={source.source}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-cinema-gold hover:underline"
                    >
                      🔗
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </motion.details>
  );
}
