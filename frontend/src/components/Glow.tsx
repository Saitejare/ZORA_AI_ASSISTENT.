import React, { memo } from 'react';
import { motion } from 'framer-motion';
import type { FaceMode } from '../types/FaceState';
import { ambientEase, glowPresets } from './Animations';

interface GlowProps {
  mode: FaceMode;
  color: string;
  /** 0..1, boosts glow further (e.g. live volume while speaking). */
  volume?: number;
  breathScale?: number;
}

/**
 * Soft holographic bloom behind the head. Two layers:
 * - an always-on slow breathing pulse (idle life-sign)
 * - a mode-reactive layer that brightens for listening/speaking/thinking,
 *   and shrinks + shifts to orange/red for error.
 */
function GlowImpl({ mode, color, volume = 0, breathScale = 1 }: GlowProps) {
  const preset = glowPresets[mode] ?? glowPresets.idle;
  const glowColor = preset.color ?? color;
  const dynamicBoost = mode === 'speaking' ? volume * 0.35 : 0;

  return (
    <div className="aiface-glow" aria-hidden="true">
      <motion.div
        className="aiface-glow__layer aiface-glow__layer--breath"
        style={{ background: `radial-gradient(circle, ${glowColor}55 0%, ${glowColor}00 70%)` }}
        animate={{ scale: [breathScale * 0.98, breathScale * 1.04, breathScale * 0.98] }}
        transition={ambientEase}
      />
      <motion.div
        className="aiface-glow__layer aiface-glow__layer--reactive"
        style={{ background: `radial-gradient(circle, ${glowColor}88 0%, ${glowColor}00 65%)` }}
        animate={{
          opacity: preset.opacity + dynamicBoost,
          scale: preset.scale + dynamicBoost * 0.3,
        }}
        transition={{ duration: 0.35, ease: 'easeOut' }}
      />
    </div>
  );
}

export const Glow = memo(GlowImpl);
export default Glow;
