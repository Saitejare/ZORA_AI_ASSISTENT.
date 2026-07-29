import React, { memo, useMemo } from 'react';
import { motion } from 'framer-motion';
import type { Emotion, FaceMode } from '../types/FaceState';
import { mouthSpring } from './Animations';

interface MouthProps {
  mode: FaceMode;
  emotion: Emotion;
  /** Smoothed 0..1 openness, already rAF-interpolated upstream. */
  openness: number;
  lipColor: string;
  cavityColor: string;
}

const BASE_HALF_WIDTH = 30;
const MAX_WIDTH_DELTA = 8;
const MAX_OPEN_HEIGHT = 26;
const SMILE_LIFT = 7;

/**
 * Builds a symmetric lip path. The command structure (M + C + C) never
 * changes, only coordinates do, which is what lets Framer Motion morph
 * smoothly between shapes frame to frame.
 */
function buildPath(halfWidth: number, topY: number, bottomY: number, cornerLift: number) {
  const left = -halfWidth;
  const right = halfWidth;
  const cornerY = -cornerLift;
  return [
    `M ${left} ${cornerY}`,
    `C ${left * 0.35} ${cornerY - topY}, ${right * 0.35} ${cornerY - topY}, ${right} ${cornerY}`,
    `C ${right * 0.35} ${cornerY + bottomY}, ${left * 0.35} ${cornerY + bottomY}, ${left} ${cornerY}`,
    'Z',
  ].join(' ');
}

function MouthImpl({ mode, emotion, openness, lipColor, cavityColor }: MouthProps) {
  const isSpeaking = mode === 'speaking';
  const isHappy = mode === 'happy' || (emotion === 'happy' && mode !== 'error' && mode !== 'sleeping');
  const isSleeping = mode === 'sleeping';

  const shape = useMemo(() => {
    if (isSleeping) {
      return { halfWidth: BASE_HALF_WIDTH * 0.7, topY: 0.5, bottomY: 0.5, cornerLift: 0, cavity: 0 };
    }
    if (isSpeaking) {
      const eased = Math.pow(openness, 0.85);
      return {
        halfWidth: BASE_HALF_WIDTH + eased * MAX_WIDTH_DELTA,
        topY: 2 + eased * (MAX_OPEN_HEIGHT * 0.35),
        bottomY: 2 + eased * (MAX_OPEN_HEIGHT * 0.65),
        cornerLift: isHappy ? SMILE_LIFT * 0.5 : 0,
        cavity: eased,
      };
    }
    if (isHappy) {
      return { halfWidth: BASE_HALF_WIDTH * 0.85, topY: 1, bottomY: 4, cornerLift: SMILE_LIFT, cavity: 0 };
    }
    return { halfWidth: BASE_HALF_WIDTH * 0.75, topY: 0.8, bottomY: 1.6, cornerLift: 0, cavity: 0 };
  }, [isSpeaking, isHappy, isSleeping, openness]);

  const lipPath = buildPath(shape.halfWidth, shape.topY, shape.bottomY, shape.cornerLift);
  // The cavity is a smaller, inset copy of the lip shape - it grows as the
  // mouth opens, reading as a dark gap between two faceted lip facets.
  const cavityPath = buildPath(
    shape.halfWidth * 0.72,
    shape.topY * shape.cavity * 0.9,
    shape.bottomY * shape.cavity * 0.9,
    shape.cornerLift * 0.6,
  );

  return (
    <g>
      <motion.path
        d={lipPath}
        animate={{ d: lipPath }}
        transition={mouthSpring}
        fill={lipColor}
        fillOpacity={0.95}
        stroke="#02060d"
        strokeWidth={1.4}
        strokeLinejoin="round"
      />
      <motion.path
        d={cavityPath}
        animate={{ d: cavityPath, opacity: shape.cavity > 0.02 ? 1 : 0 }}
        transition={mouthSpring}
        fill={cavityColor}
      />
    </g>
  );
}

export const Mouth = memo(MouthImpl);
export default Mouth;
