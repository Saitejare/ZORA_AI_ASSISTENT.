import React, { memo } from 'react';
import { motion } from 'framer-motion';
import FaceMesh from './FaceMesh';
import LandmarkNetwork from './LandmarkNetwork';
import Eyes from './Eyes';
import Mouth from './Mouth';
import type { Emotion, FaceMode, Vec2 } from '../types/FaceState';
import { listeningPulseVariants, softSpring } from './Animations';

interface HeadProps {
  mode: FaceMode;
  emotion: Emotion;
  idleGaze: Vec2;
  isBlinking: boolean;
  mouthOpenness: number;
  thinkingAngle: number;
  accentColor: string;
}

const ERROR_COLOR = '#ff8a4d';
const LIP_COLOR = '#4a86c2';
const CAVITY_COLOR = '#02060d';
const NOSE_LIGHT = '#3f74ab';
const NOSE_MID = '#22456d';

function HeadImpl({ mode, emotion, idleGaze, isBlinking, mouthOpenness, thinkingAngle, accentColor }: HeadProps) {
  const isError = mode === 'error';
  const isThinking = mode === 'thinking';
  const isListening = mode === 'listening';
  const isSpeaking = mode === 'speaking';
  const isHappy = mode === 'happy' || emotion === 'happy';
  const color = isError ? ERROR_COLOR : accentColor;

  const tintColor = isError ? ERROR_COLOR : accentColor;
  const tintStrength = isListening ? 0.24 : isThinking ? 0.16 : isSpeaking ? 0.14 : isError ? 0.22 : 0.05;
  const landmarkIntensity = isListening ? 1 : isThinking ? 0.6 : 0.25;

  const chinOffset = isSpeaking ? mouthOpenness * 3 : 0;
  const browFurrow = isThinking || isError;
  const browRaise = isHappy && !isError;

  return (
    <g>
      {/* Faint constellation network sits behind the solid mesh so it only
          peeks out around the silhouette edges, like the reference image. */}
      <LandmarkNetwork color={accentColor} intensity={landmarkIntensity} />

      {/* Listening halo pulse */}
      <motion.circle
        cx={0}
        cy={-14}
        r={150}
        fill="none"
        stroke={color}
        strokeWidth={1.5}
        variants={listeningPulseVariants}
        animate={isListening ? 'active' : 'idle'}
      />

      {/* Thinking orbit dots */}
      {[0, 120, 240].map((offset) => {
        const rad = ((thinkingAngle + offset) * Math.PI) / 180;
        const rx = 128;
        const ry = 150;
        const x = Math.cos(rad) * rx;
        const y = -14 + Math.sin(rad) * ry * 0.55;
        return (
          <motion.circle
            key={offset}
            cx={x}
            cy={y}
            r={4}
            fill={color}
            animate={{ opacity: isThinking ? 0.9 : 0 }}
            transition={{ duration: 0.3 }}
          />
        );
      })}

      {/* Solid faceted head/face mesh */}
      <motion.g style={{ translateY: chinOffset }}>
        <FaceMesh tintColor={tintColor} tintStrength={tintStrength} />
      </motion.g>

      {/* Eyebrows: small faceted wedges above each eye */}
      <motion.polygon
        points="-48,-38 -14,-46 -30,-32"
        fill="#02060d"
        opacity={0.92}
        animate={{
          y: browRaise ? -8 : browFurrow ? 6 : 0,
          rotate: browFurrow ? 6 : 0,
        }}
        style={{ transformOrigin: '-30px -38px' }}
        transition={softSpring}
      />
      <motion.polygon
        points="48,-38 14,-46 30,-32"
        fill="#02060d"
        opacity={0.92}
        animate={{
          y: browRaise ? -8 : browFurrow ? 6 : 0,
          rotate: browFurrow ? -6 : 0,
        }}
        style={{ transformOrigin: '30px -38px' }}
        transition={softSpring}
      />

      {/* Eyes */}
      <Eyes mode={mode} idleGaze={idleGaze} isBlinking={isBlinking} accentColor={accentColor} />

      {/* Nose: a few small faceted planes for a subtle 3D bridge/tip */}
      <g opacity={0.95}>
        <polygon points="0,-6 -7,20 0,30" fill={NOSE_LIGHT} />
        <polygon points="0,-6 0,30 7,20" fill={NOSE_MID} />
        <polygon points="-7,20 -10,26 0,30" fill="#0d2038" />
        <polygon points="7,20 0,30 10,26" fill="#132c4a" />
      </g>

      {/* Mouth, jaw/chin follows via the shared translateY offset above */}
      <motion.g style={{ translateY: chinOffset }} transform="translate(0, 60)">
        <Mouth mode={mode} emotion={emotion} openness={mouthOpenness} lipColor={LIP_COLOR} cavityColor={CAVITY_COLOR} />
      </motion.g>
    </g>
  );
}

export const Head = memo(HeadImpl);
export default Head;
