import React, { memo } from 'react';
import { motion } from 'framer-motion';
import type { Vec2 } from '../types/FaceState';
import { softSpring } from './Animations';

interface EyeProps {
  /** Mirrors the shape horizontally for the left/right pair. */
  side: 'left' | 'right';
  gaze: Vec2;
  isBlinking: boolean;
  /** Fully shut, e.g. while sleeping - independent of the transient blink. */
  isClosed: boolean;
  /** 0..1, brightens the glint + faint inner glow (e.g. while listening). */
  brightness: number;
  /** true while happy -> softened, slightly squinted almond shape. */
  soft: boolean;
  /** Facet-toned color used for the eyelid so it reads as part of the mesh. */
  lidColor: string;
  /** Deep, near-background shade used for the open eye socket. */
  socketColor: string;
  /** Accent color used only for the subtle gaze glint. */
  accentColor: string;
}

// A dark, almond-shaped negative-space socket - the low-poly face's "eye"
// is simply an absence of facets, matching the reference image.
const SOCKET_NEUTRAL = 'M -22 8 C -14 -4, 14 -4, 22 8 C 14 19, -14 19, -22 8 Z';
const SOCKET_SOFT = 'M -22 10 C -14 2, 14 2, 22 10 C 14 17, -14 17, -22 10 Z';

function EyeImpl({ side, gaze, isBlinking, isClosed, brightness, soft, lidColor, socketColor, accentColor }: EyeProps) {
  const mirror = side === 'left' ? -1 : 1;
  const showClosed = isClosed || isBlinking;
  const socketPath = soft ? SOCKET_SOFT : SOCKET_NEUTRAL;

  return (
    <g transform={`scale(${mirror}, 1)`}>
      <clipPath id={`eye-clip-${side}`}>
        <motion.path d={socketPath} animate={{ d: socketPath }} transition={softSpring} />
      </clipPath>

      {/* The socket itself - a flat dark cutout, no visible iris ring. A
          faint rim keeps it legible against the mesh's own dark facets. */}
      <motion.path
        d={socketPath}
        fill={socketColor}
        stroke="rgba(150, 195, 240, 0.22)"
        strokeWidth={0.8}
        animate={{ d: socketPath }}
        transition={softSpring}
      />

      {/* A faint, low-opacity glint that drifts with gaze - just enough to
          read as "looking," without breaking the plain-socket aesthetic. */}
      <g clipPath={`url(#eye-clip-${side})`}>
        <motion.circle
          cx={0}
          cy={0}
          r={5}
          fill={accentColor}
          animate={{
            x: gaze.x * mirror,
            y: gaze.y,
            opacity: 0.08 + brightness * 0.32,
          }}
          transition={{ type: 'spring', stiffness: 90, damping: 16 }}
        />
      </g>

      {/* Eyelid: same tone as the surrounding facets, slides down to close. */}
      <motion.rect
        x={-26}
        y={-16}
        width={52}
        height={32}
        fill={lidColor}
        style={{ transformOrigin: '0px -16px' }}
        animate={{ scaleY: showClosed ? 1 : 0 }}
        transition={isBlinking ? { duration: 0.09, ease: 'easeInOut' } : softSpring}
      />
    </g>
  );
}

export const Eye = memo(EyeImpl);
export default Eye;
