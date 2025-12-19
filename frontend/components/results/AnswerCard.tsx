'use client';

import { motion } from 'framer-motion';

interface AnswerCardProps {
  answer: string;
}

export default function AnswerCard({ answer }: AnswerCardProps) {
  return (
    <motion.div
      className="bg-cinema-dark border border-cinema-gold rounded-lg p-5"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h2 className="text-lg font-bold text-cinema-gold mb-3">✨ Answer</h2>
      <p className="text-cinema-white leading-relaxed text-sm">{answer}</p>
    </motion.div>
  );
}
