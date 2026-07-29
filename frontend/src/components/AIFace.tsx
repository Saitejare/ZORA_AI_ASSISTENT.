import React, { memo, useMemo } from 'react';
import { motion } from 'framer-motion';
import Background from './Background';
import Glow from './Glow';
import Head from './Head';
import { useBlink } from '../hooks/useBlink';
import { useVoice } from '../hooks/useVoice';
import { useIdle } from '../hooks/useIdle';
import { useThinking } from '../hooks/useThinking';
import type { AIFaceProps, FaceMode } from '../types/FaceState';
import { faceContainerVariants } from './Animations';
import '../styles/aiface.css';

const DEFAULT_ACCENT = '#4da8ff';

/** Resolves the (possibly overlapping) boolean props into one exclusive mode. */
function resolveMode(props: Required<Pick<AIFaceProps, 'isSleeping' | 'isSpeaking' | 'isListening' | 'isThinking' | 'emotion'>>): FaceMode {
  if (props.isSleeping) return 'sleeping';
  if (props.emotion === 'error') return 'error';
  if (props.isSpeaking) return 'speaking';
  if (props.isListening) return 'listening';
  if (props.isThinking) return 'thinking';
  if (props.emotion === 'happy') return 'happy';
  return 'idle';
}

/**
 * <AIFace /> - a minimal, futuristic holographic AI face.
 *
 * Renders entirely with SVG (face geometry) + HTML5 Canvas (ambient
 * particles) + CSS (glow, layout) animated with Framer Motion. No external
 * models, images, or animation software involved.
 */
function AIFaceImpl({
  isSpeaking = false,
  isListening = false,
  isThinking = false,
  emotion = 'neutral',
  audioLevel = 0,
  volume = 0,
  isSleeping = false,
  accentColor = DEFAULT_ACCENT,
  size = '100%',
  className = '',
  name = 'BERU',
}: AIFaceProps) {
  const mode = useMemo(
    () => resolveMode({ isSleeping, isSpeaking, isListening, isThinking, emotion }),
    [isSleeping, isSpeaking, isListening, isThinking, emotion],
  );

  const { isBlinking } = useBlink({ enabled: mode !== 'sleeping' });
  const { mouthOpenness } = useVoice({ audioLevel, isSpeaking: mode === 'speaking' });
  const { floatY, breathScale, gaze } = useIdle({ enabled: mode !== 'sleeping' });
  const { angle: thinkingAngle } = useThinking({ enabled: mode === 'thinking' });

  const containerStyle = useMemo(
    () =>
      ({
        width: size,
        height: size,
        '--face-accent': accentColor,
      }) as React.CSSProperties,
    [size, accentColor],
  );

  return (
    <div className={`aiface-root ${className}`} style={containerStyle} data-mode={mode}>
      <Background active={mode === 'listening'} accentColor={accentColor}>
        <motion.div
          className="aiface-stage"
          variants={faceContainerVariants}
          initial="hidden"
          animate="visible"
        >
          <Glow mode={mode} color={accentColor} volume={volume} breathScale={breathScale} />
          <motion.svg
            viewBox="-140 -170 280 320"
            className="aiface-svg"
            style={{ translateY: mode === 'sleeping' ? 0 : floatY, scale: breathScale }}
            role="img"
            aria-label={`${name}, AI assistant face, currently ${mode}`}
          >
            <Head
              mode={mode}
              emotion={emotion}
              idleGaze={gaze}
              isBlinking={isBlinking}
              mouthOpenness={mouthOpenness}
              thinkingAngle={thinkingAngle}
              accentColor={accentColor}
            />
          </motion.svg>
        </motion.div>
      </Background>
    </div>
  );
}

export const AIFace = memo(AIFaceImpl);
export default AIFace;
