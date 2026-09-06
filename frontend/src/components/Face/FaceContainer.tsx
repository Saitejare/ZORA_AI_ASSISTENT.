import React from 'react';
import { motion } from 'framer-motion';
import { faceFloatVariants, pulseRingVariants } from '../../animations/variants';
import { useBlink } from '../../hooks/useBlink';
import { HolographicEyes } from './Eyes/HolographicEyes';
import { HeadStructure } from './HeadStructure';
import { AudioMouth } from './Mouth/AudioMouth';

interface FaceContainerProps {
  state: string;
  audioLevel: number;
}

export const FaceContainer: React.FC<FaceContainerProps> = React.memo(({ state, audioLevel }) => {
  const isBlinking = useBlink(state);

  return (
    <div className="face-container">
      <motion.div className="face-pulse-ring hologram-glow" variants={pulseRingVariants} animate="animate" />

      {state === 'Thinking' && (
        <motion.div className="face-radar face-radar--thinking" animate={{ rotate: 360 }} transition={{ duration: 8, repeat: Infinity, ease: 'linear' }} />
      )}

      {state === 'Searching' && (
        <motion.div className="face-radar face-radar--searching" animate={{ rotate: 360 }} transition={{ duration: 2, repeat: Infinity, ease: 'linear' }} />
      )}

      <motion.svg viewBox="0 0 400 420" className="face-svg" variants={faceFloatVariants} animate={state}>
        <HeadStructure state={state} audioLevel={audioLevel} />
        <HolographicEyes isBlinking={isBlinking} state={state} audioLevel={audioLevel} />
        <AudioMouth state={state} audioLevel={audioLevel} />
      </motion.svg>
    </div>
  );
});

FaceContainer.displayName = 'FaceContainer';
