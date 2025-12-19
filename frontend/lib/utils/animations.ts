import { Variants } from 'framer-motion';

// Page-level animations
export const pageVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      duration: 0.6,
      ease: 'easeOut',
      staggerChildren: 0.1,
    },
  },
};

export const fadeInUp: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.5,
      ease: 'easeOut',
    },
  },
};

// Movie card animations
export const movieCardVariants: Variants = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: {
      duration: 0.4,
      ease: 'easeOut',
    },
  },
  hover: {
    scale: 1.05,
    rotateY: 5,
    transition: {
      type: 'spring',
      stiffness: 300,
      damping: 20,
    },
  },
  tap: {
    scale: 0.98,
  },
};

// Grid stagger animations
export const gridContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0,
    },
  },
};

export const gridItemVariants: Variants = {
  hidden: { opacity: 0, y: 10, scale: 0.98 },
  visible: {
    opacity: 1,
    y: 0,
    scale: 1,
    transition: {
      duration: 0.3,
      ease: [0.25, 0.46, 0.45, 0.94], // Custom easing
    },
  },
};

// Search hero animations
export const searchBarVariants: Variants = {
  rest: { scale: 1 },
  focus: {
    scale: 1.02,
    transition: {
      duration: 0.2,
      ease: 'easeOut',
    },
  },
};

export const buttonVariants: Variants = {
  rest: { scale: 1 },
  hover: {
    scale: 1.05,
    transition: {
      duration: 0.2,
      ease: 'easeOut',
    },
  },
  tap: {
    scale: 0.95,
  },
};

// Processing step animations
export const processingVariants: Variants = {
  hidden: { opacity: 0, x: -10 },
  visible: {
    opacity: 1,
    x: 0,
    transition: {
      duration: 0.3,
      ease: 'easeOut',
    },
  },
  exit: {
    opacity: 0,
    x: 10,
    transition: {
      duration: 0.2,
    },
  },
};

// Answer card animations
export const answerCardVariants: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  },
};

// Backdrop reveal animation (for movie cards)
export const backdropVariants: Variants = {
  hidden: { opacity: 0, scale: 1.1 },
  visible: {
    opacity: 0.2,
    scale: 1.1,
    transition: {
      duration: 0.3,
    },
  },
};

// Poster animation
export const posterVariants: Variants = {
  rest: { scale: 1 },
  hover: {
    scale: 1.05,
    transition: {
      duration: 0.3,
      ease: 'easeOut',
    },
  },
};

// Helper: Check if user prefers reduced motion
export function shouldReduceMotion(): boolean {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

// Helper: Get animation props (returns empty object if reduced motion)
export function getAnimationProps(variants: Variants, initial = 'hidden', animate = 'visible') {
  if (shouldReduceMotion()) {
    return {};
  }
  return {
    initial,
    animate,
    variants,
  };
}
