import { useEffect, useRef, useState } from 'react';

interface UseThinkingOptions {
  enabled: boolean;
  /** Degrees per second for the orbiting dots. */
  speedDegPerSec?: number;
}

interface ThinkingState {
  /** Current rotation angle in degrees for the orbiting dot ring. */
  angle: number;
}

/**
 * Advances a rotation angle continuously while `enabled` is true so the
 * "thinking" orbit dots sweep smoothly around the head. Pauses (and keeps
 * the last angle) as soon as thinking stops, so it doesn't jump on re-entry.
 */
export function useThinking({ enabled, speedDegPerSec = 60 }: UseThinkingOptions): ThinkingState {
  const [angle, setAngle] = useState(0);
  const rafRef = useRef<number>(0);
  const lastRef = useRef<number | null>(null);

  useEffect(() => {
    if (!enabled) {
      lastRef.current = null;
      return;
    }

    const loop = (t: number) => {
      if (lastRef.current == null) lastRef.current = t;
      const dt = (t - lastRef.current) / 1000;
      lastRef.current = t;
      setAngle((prev) => (prev + speedDegPerSec * dt) % 360);
      rafRef.current = requestAnimationFrame(loop);
    };

    rafRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(rafRef.current);
  }, [enabled, speedDegPerSec]);

  return { angle };
}
