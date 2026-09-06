import type { Variants } from 'framer-motion';

export const faceFloatVariants: Variants = {
  Idle: {
    y: [0, -10, 0],
    transition: { duration: 6, repeat: Infinity, ease: 'easeInOut' },
  },
  Listening: {
    scale: 1.03,
    y: [0, -5, 0],
    transition: { duration: 2, repeat: Infinity, ease: 'easeInOut' },
  },
  Recognizing: {
    scale: 1.01,
    transition: { duration: 1.4, repeat: Infinity, ease: 'easeInOut' },
  },
  Thinking: {
    rotate: [0, 1, -1, 0],
    transition: { duration: 3, repeat: Infinity, ease: 'easeInOut' },
  },
  Speaking: {
    y: [0, -4, 0],
    transition: { duration: 0.8, repeat: Infinity, ease: 'easeInOut' },
  },
  Searching: {
    scale: [1, 1.02, 1],
    transition: { duration: 2, repeat: Infinity, ease: 'easeInOut' },
  },
  Executing: {
    rotate: [0, -1, 1, 0],
    transition: { duration: 2.4, repeat: Infinity, ease: 'easeInOut' },
  },
  Happy: {
    y: [0, -12, 0],
    transition: { duration: 2.8, repeat: Infinity, ease: 'easeInOut' },
  },
  Error: {
    x: [0, -2, 2, 0],
    transition: { duration: 0.22, repeat: Infinity },
  },
  Sleeping: {
    y: 10,
    opacity: 0.7,
    transition: { duration: 2 },
  },
};

export const pulseRingVariants: Variants = {
  animate: {
    scale: [1, 1.35, 1],
    opacity: [0.2, 0.6, 0.2],
    transition: { duration: 2.5, repeat: Infinity, ease: 'easeInOut' },
  },
};
