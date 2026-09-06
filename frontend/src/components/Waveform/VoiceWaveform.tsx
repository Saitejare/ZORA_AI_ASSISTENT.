import React, { useEffect, useRef } from 'react';
import { useVoiceWave } from '../../hooks/useVoiceWave';

interface VoiceWaveformProps {
  audioLevel: number;
  state: string;
}

const statusByState: Record<string, string> = {
  Idle: 'Awaiting Input',
  Listening: 'Listening...',
  Recognizing: 'Recognizing Speech...',
  Thinking: 'Thinking...',
  Speaking: 'Speaking...',
  Searching: 'Searching Network...',
  Executing: 'Executing Task...',
  Happy: 'ZORA Active',
  Error: 'System Exception',
  Sleeping: 'Standby Mode',
};

export const VoiceWaveform: React.FC<VoiceWaveformProps> = React.memo(({ audioLevel, state }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (canvasRef.current) {
      canvasRef.current.width = 600;
      canvasRef.current.height = 100;
    }
  }, []);

  useVoiceWave(canvasRef, audioLevel, state);

  return (
    <div className="voice-waveform">
      <canvas ref={canvasRef} className="voice-waveform__canvas" />
      <span className="voice-waveform__label">{statusByState[state]}</span>
    </div>
  );
});

VoiceWaveform.displayName = 'VoiceWaveform';
