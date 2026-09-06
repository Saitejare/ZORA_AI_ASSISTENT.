import React from 'react';
import { motion } from 'framer-motion';

interface HolographicEyesProps {
  isBlinking: boolean;
  state: string;
  audioLevel: number;
}

export const HolographicEyes: React.FC<HolographicEyesProps> = React.memo(({ isBlinking, state, audioLevel }) => {
  const isError = state === 'Error';
  const isHappy = state === 'Happy';
  const isSleeping = state === 'Sleeping';

  const primaryColor = isError ? '#ff5500' : '#00f0ff';
  const secondaryColor = isError ? '#ff0055' : '#7000ff';
  const isVoiceReactive = state === 'Speaking' || state === 'Listening' || state === 'Recognizing';
  const eyeScaleY = isBlinking || isSleeping ? 0.05 : isHappy ? 0.6 : isError ? 0.75 : 1 - audioLevel * 0.12;
  const pupilScale = isVoiceReactive ? 1 + audioLevel * 0.9 : 1;
  const pupilOffsetX = isVoiceReactive ? Math.sin(Date.now() * 0.012) * audioLevel * 5 : 0;
  const pupilOffsetY = isVoiceReactive ? Math.cos(Date.now() * 0.01) * audioLevel * 3 : 0;
  const eyeLift = isVoiceReactive ? -audioLevel * 4 : 0;

  return (
    <g id="holographic-eyes">
      <motion.path
        d={isHappy ? 'M 130 165 Q 160 150 190 165' : isError ? 'M 130 175 Q 160 185 190 170' : 'M 130 160 Q 160 155 190 162'}
        stroke={primaryColor}
        strokeWidth="2.5"
        fill="none"
        strokeLinecap="round"
        opacity="0.85"
        animate={{
          d: isHappy ? 'M 130 165 Q 160 150 190 165' : isError ? 'M 130 175 Q 160 185 190 170' : 'M 130 160 Q 160 155 190 162',
        }}
      />
      <motion.path
        d={isHappy ? 'M 210 165 Q 240 150 270 165' : isError ? 'M 210 170 Q 240 185 270 175' : 'M 210 162 Q 240 155 270 160'}
        stroke={primaryColor}
        strokeWidth="2.5"
        fill="none"
        strokeLinecap="round"
        opacity="0.85"
        animate={{
          d: isHappy ? 'M 210 165 Q 240 150 270 165' : isError ? 'M 210 170 Q 240 185 270 175' : 'M 210 162 Q 240 155 270 160',
        }}
      />

      <motion.g transform="translate(160, 195)" animate={{ y: eyeLift }} transition={{ duration: 0.08 }}>
        <motion.g animate={{ scaleY: eyeScaleY }} transition={{ duration: 0.08 }}>
          <circle r="22" fill="none" stroke={primaryColor} strokeWidth="1.5" opacity="0.6" strokeDasharray="6 3" />
          <circle r="16" fill="none" stroke={secondaryColor} strokeWidth="1" opacity="0.8" />
          <motion.circle r="7" fill={primaryColor} opacity="0.9" animate={{ scale: pupilScale, x: pupilOffsetX, y: pupilOffsetY }} />
          <motion.circle r="3" fill="#ffffff" opacity="0.9" animate={{ x: pupilOffsetX - 2, y: pupilOffsetY - 2 }} />
        </motion.g>
      </motion.g>

      <motion.g transform="translate(240, 195)" animate={{ y: eyeLift }} transition={{ duration: 0.08 }}>
        <motion.g animate={{ scaleY: eyeScaleY }} transition={{ duration: 0.08 }}>
          <circle r="22" fill="none" stroke={primaryColor} strokeWidth="1.5" opacity="0.6" strokeDasharray="6 3" />
          <circle r="16" fill="none" stroke={secondaryColor} strokeWidth="1" opacity="0.8" />
          <motion.circle r="7" fill={primaryColor} opacity="0.9" animate={{ scale: pupilScale, x: pupilOffsetX, y: pupilOffsetY }} />
          <motion.circle r="3" fill="#ffffff" opacity="0.9" animate={{ x: pupilOffsetX - 2, y: pupilOffsetY - 2 }} />
        </motion.g>
      </motion.g>
    </g>
  );
});

HolographicEyes.displayName = 'HolographicEyes';
