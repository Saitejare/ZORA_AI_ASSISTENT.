import React, { memo } from 'react';
import Eye from './Eye';
import type { FaceMode, Vec2 } from '../types/FaceState';

interface EyesProps {
  mode: FaceMode;
  idleGaze: Vec2;
  isBlinking: boolean;
  accentColor: string;
}

const ERROR_COLOR = '#ff8a4d';
const SOCKET_COLOR = '#02060d';
const LID_COLOR = '#234876';
const EYE_SPACING = 58;
const EYE_Y = 0;

/**
 * Resolves the current mode into a gaze target, glint brightness, and
 * color, then renders the mirrored pair of <Eye/> sockets.
 *
 * - speaking: eyes stay focused (locked to center, no drift)
 * - thinking: gaze glances slightly upward
 * - listening: glint brightens
 * - error: glint shifts to orange
 * - sleeping: fully closed
 */
function EyesImpl({ mode, idleGaze, isBlinking, accentColor }: EyesProps) {
  const isClosed = mode === 'sleeping';
  const isSoft = mode === 'happy';
  const isError = mode === 'error';

  let gaze: Vec2 = idleGaze;
  if (mode === 'speaking') gaze = { x: 0, y: 0 };
  if (mode === 'thinking') gaze = { x: idleGaze.x * 0.4, y: -8 };
  if (mode === 'listening') gaze = { x: 0, y: 0 };

  const brightness = mode === 'listening' ? 1 : mode === 'error' ? 0.15 : 0.25;
  const glintColor = isError ? ERROR_COLOR : accentColor;

  return (
    <g>
      <g transform={`translate(${-EYE_SPACING / 2}, ${EYE_Y})`}>
        <Eye
          side="left"
          gaze={gaze}
          isBlinking={isBlinking}
          isClosed={isClosed}
          brightness={brightness}
          soft={isSoft}
          lidColor={LID_COLOR}
          socketColor={SOCKET_COLOR}
          accentColor={glintColor}
        />
      </g>
      <g transform={`translate(${EYE_SPACING / 2}, ${EYE_Y})`}>
        <Eye
          side="right"
          gaze={gaze}
          isBlinking={isBlinking}
          isClosed={isClosed}
          brightness={brightness}
          soft={isSoft}
          lidColor={LID_COLOR}
          socketColor={SOCKET_COLOR}
          accentColor={glintColor}
        />
      </g>
    </g>
  );
}

export const Eyes = memo(EyesImpl);
export default Eyes;
