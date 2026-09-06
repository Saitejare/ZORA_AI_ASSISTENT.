import React from 'react';
import { motion } from 'framer-motion';

interface HeadStructureProps {
  state: string;
  audioLevel: number;
}

export const HeadStructure: React.FC<HeadStructureProps> = React.memo(({ state, audioLevel }) => {
  const isError = state === 'Error';
  const primaryColor = isError ? '#ff5500' : '#00f0ff';
  const secondaryColor = isError ? '#ff0055' : '#0066ff';
  const accentColor = '#7000ff';

  return (
    <g id="holographic-head-frame">
      <circle cx="200" cy="210" r="170" fill="none" stroke={primaryColor} strokeWidth="1" opacity="0.25" strokeDasharray="4 8" />

      <motion.circle
        cx="200"
        cy="210"
        r="155"
        fill="none"
        stroke={secondaryColor}
        strokeWidth="1.5"
        opacity="0.4"
        strokeDasharray="40 10 15 10"
        animate={{ rotate: 360 }}
        transition={{ duration: 30, repeat: Infinity, ease: 'linear' }}
        style={{ originX: '200px', originY: '210px' }}
      />

      <path
        d="M 120 140 C 120 90, 280 90, 280 140 C 290 190, 285 240, 265 285 C 250 320, 225 345, 200 350 C 175 345, 150 320, 135 285 C 115 240, 110 190, 120 140 Z"
        fill="url(#headGradient)"
        stroke={primaryColor}
        strokeWidth="2"
        opacity="0.85"
      />

      <path d="M 130 180 L 105 195 L 105 230 L 125 250" fill="none" stroke={secondaryColor} strokeWidth="1.2" opacity="0.6" />
      <path d="M 270 180 L 295 195 L 295 230 L 275 250" fill="none" stroke={secondaryColor} strokeWidth="1.2" opacity="0.6" />
      <path d="M 196 195 L 200 235 L 204 195" fill="none" stroke={primaryColor} strokeWidth="1.2" opacity="0.5" />
      <path d="M 193 240 L 200 245 L 207 240" fill="none" stroke={primaryColor} strokeWidth="1.5" opacity="0.7" />

      <motion.path
        d="M 155 315 L 200 335 L 245 315"
        fill="none"
        stroke={accentColor}
        strokeWidth="1.5"
        opacity="0.7"
        animate={{ translateY: state === 'Speaking' ? audioLevel * 3 : 0 }}
      />

      <defs>
        <radialGradient id="headGradient" cx="50%" cy="40%" r="60%">
          <stop offset="0%" stopColor="#00f0ff" stopOpacity="0.12" />
          <stop offset="70%" stopColor="#0066ff" stopOpacity="0.04" />
          <stop offset="100%" stopColor="#050816" stopOpacity="0.8" />
        </radialGradient>
      </defs>
    </g>
  );
});

HeadStructure.displayName = 'HeadStructure';
