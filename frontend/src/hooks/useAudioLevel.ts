import { useEffect, useState } from 'react';

export const useAudioLevel = (state: string, externalAudioLevel?: number) => {
  const [audioLevel, setAudioLevel] = useState(0);

  useEffect(() => {
    if (externalAudioLevel !== undefined) {
      setAudioLevel(externalAudioLevel);
      return;
    }

    let animationFrameId: number;

    const simulateAudio = () => {
      if (state === 'Speaking') {
        const time = Date.now() * 0.008;
        const level =
          (Math.sin(time) * 0.4 + Math.cos(time * 2.3) * 0.3 + 0.3) *
          (0.6 + Math.random() * 0.4);
        setAudioLevel(Math.max(0.1, Math.min(1, level)));
      } else if (state === 'Listening') {
        setAudioLevel(0.1 + Math.random() * 0.2);
      } else {
        setAudioLevel(0);
      }

      animationFrameId = requestAnimationFrame(simulateAudio);
    };

    animationFrameId = requestAnimationFrame(simulateAudio);

    return () => cancelAnimationFrame(animationFrameId);
  }, [state, externalAudioLevel]);

  return audioLevel;
};
