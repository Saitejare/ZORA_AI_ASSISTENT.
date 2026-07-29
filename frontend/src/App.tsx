import React, { useEffect, useRef, useState } from 'react';
import AIFace from './components/AIFace';
import type { Emotion } from './types/FaceState';

type Mode = 'idle' | 'listening' | 'thinking' | 'speaking' | 'sleeping';

/**
 * Demo harness for <AIFace/>. Not part of the reusable component API -
 * just a control panel so every state can be exercised and previewed.
 */
export default function App() {
  const [mode, setMode] = useState<Mode>('idle');
  const [emotion, setEmotion] = useState<Emotion>('neutral');
  const [audioLevel, setAudioLevel] = useState(0);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const rafRef = useRef<number>(0);

  // While "speaking" + auto mode, fake a plausible audio waveform so the
  // mouth has something reactive to animate to without real mic/TTS input.
  useEffect(() => {
    if (mode !== 'speaking' || !autoSpeak) return;
    let t = 0;
    const tick = () => {
      t += 0.06;
      const level = Math.max(0, Math.sin(t * 3) * 0.5 + Math.sin(t * 7.3) * 0.25 + 0.4);
      setAudioLevel(Math.min(1, level));
      rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [mode, autoSpeak]);

  const modes: Mode[] = ['idle', 'listening', 'thinking', 'speaking', 'sleeping'];
  const emotions: Emotion[] = ['neutral', 'happy', 'error'];

  return (
    <div className="app-shell">
      <div className="app-stage">
        <div className="app-stage__face">
          <AIFace
            isSpeaking={mode === 'speaking'}
            isListening={mode === 'listening'}
            isThinking={mode === 'thinking'}
            isSleeping={mode === 'sleeping'}
            emotion={emotion}
            audioLevel={audioLevel}
            volume={audioLevel}
          />
        </div>
      </div>

      <aside className="app-panel">
        <h1>BERU</h1>
        <p>Holographic AI assistant — drive every state to preview its animation set.</p>

        <div className="app-panel__group">
          <label>Mode</label>
          <div className="app-panel__buttons">
            {modes.map((m) => (
              <button key={m} data-active={mode === m} onClick={() => setMode(m)}>
                {m}
              </button>
            ))}
          </div>
        </div>

        <div className="app-panel__group">
          <label>Emotion</label>
          <div className="app-panel__buttons">
            {emotions.map((e) => (
              <button key={e} data-active={emotion === e} onClick={() => setEmotion(e)}>
                {e}
              </button>
            ))}
          </div>
        </div>

        <div className="app-panel__group">
          <label>
            Audio level
            <span className="app-panel__value">{audioLevel.toFixed(2)}</span>
          </label>
          <input
            type="range"
            min={0}
            max={1}
            step={0.01}
            value={audioLevel}
            disabled={mode === 'speaking' && autoSpeak}
            onChange={(e) => setAudioLevel(Number(e.target.value))}
          />
        </div>

        <div className="app-panel__group">
          <label>
            <input
              type="checkbox"
              checked={autoSpeak}
              onChange={(e) => setAutoSpeak(e.target.checked)}
              style={{ marginRight: 8 }}
            />
            Auto-simulate speech waveform
          </label>
        </div>
      </aside>
    </div>
  );
}
