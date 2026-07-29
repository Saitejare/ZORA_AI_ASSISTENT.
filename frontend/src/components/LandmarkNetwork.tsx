import React, { memo } from 'react';
import { motion } from 'framer-motion';
import { LANDMARKS, LANDMARK_EDGES } from './faceGeometry';

interface LandmarkNetworkProps {
  color: string;
  /** 0..1, how bright/active the nodes glow (rises while listening/thinking). */
  intensity: number;
}

const NAMES = Object.keys(LANDMARKS);

/**
 * Draws the faint "scan mesh" lines between bone landmarks and the glowing
 * node at each one, matching the reference image's constellation overlay
 * that sits on top of the solid faceted head.
 */
function LandmarkNetworkImpl({ color, intensity }: LandmarkNetworkProps) {
  return (
    <g>
      {LANDMARK_EDGES.map(([a, b], i) => {
        const pa = LANDMARKS[a];
        const pb = LANDMARKS[b];
        return (
          <line
            key={i}
            x1={pa.x}
            y1={pa.y}
            x2={pb.x}
            y2={pb.y}
            stroke={color}
            strokeWidth={0.75}
            strokeOpacity={0.22 + intensity * 0.18}
          />
        );
      })}
      {NAMES.map((name, i) => {
        const p = LANDMARKS[name];
        return (
          <g key={name}>
            <circle cx={p.x} cy={p.y} r={5.5} fill={color} opacity={0.12 + intensity * 0.18} />
            <motion.circle
              cx={p.x}
              cy={p.y}
              r={2}
              fill={color}
              animate={{
                opacity: [0.7, 1, 0.7],
                r: [1.7, 2.2, 1.7],
              }}
              transition={{
                duration: 2.4 + (i % 5) * 0.3,
                repeat: Infinity,
                ease: 'easeInOut',
                delay: (i % 7) * 0.2,
              }}
            />
          </g>
        );
      })}
    </g>
  );
}

export const LandmarkNetwork = memo(LandmarkNetworkImpl);
export default LandmarkNetwork;
