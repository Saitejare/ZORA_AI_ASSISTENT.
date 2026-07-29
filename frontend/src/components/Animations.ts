import type { Transition, Variants } from 'framer-motion';

/**
 * Central place for reusable Framer Motion variants/transitions so every
 * component animates with a consistent, tuned feel instead of ad-hoc
 * numbers scattered across files.
 */

/** Smooth, physically-plausible spring used for expressive state changes. */
export const softSpring: Transition = {
  type: 'spring',
  stiffness: 120,
  damping: 14,
  mass: 0.6,
};

/** Snappier spring for the mouth, which needs to track audio closely. */
export const mouthSpring: Transition = {
  type: 'spring',
  stiffness: 260,
  damping: 20,
  mass: 0.4,
};

/** Slow ease used for glow/breathing style ambient loops. */
export const ambientEase: Transition = {
  duration: 4,
  repeat: Infinity,
  ease: 'easeInOut',
};

/** Container-level float/appear variants for the whole face. */
export const faceContainerVariants: Variants = {
  hidden: { opacity: 0, scale: 0.92 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.6, ease: 'easeOut' },
  },
};

/** Eyelid variants: open vs a natural blink close. */
export const eyelidVariants: Variants = {
  open: { scaleY: 1 },
  closed: { scaleY: 0.02 },
};

/** Listening halo ring pulse. */
export const listeningPulseVariants: Variants = {
  idle: { opacity: 0, scale: 0.9 },
  active: {
    opacity: [0.0, 0.55, 0],
    scale: [0.9, 1.25, 1.45],
    transition: { duration: 1.8, repeat: Infinity, ease: 'easeOut' },
  },
};

/** Glow opacity/scale presets keyed by face mode; consumed by <Glow/>. */
export const glowPresets: Record<string, { opacity: number; scale: number; color?: string }> = {
  idle: { opacity: 0.55, scale: 1 },
  listening: { opacity: 0.8, scale: 1.12 },
  thinking: { opacity: 0.7, scale: 1.05 },
  speaking: { opacity: 0.9, scale: 1.15 },
  happy: { opacity: 0.75, scale: 1.08 },
  error: { opacity: 0.35, scale: 0.95, color: '#ff5c3d' },
  sleeping: { opacity: 0.25, scale: 0.9 },
};
