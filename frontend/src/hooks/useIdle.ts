import { useEffect, useRef, useState } from 'react';
import type { Vec2 } from '../types/FaceState';

interface UseIdleOptions {
  enabled?: boolean;
}

interface IdleState {
  /** Vertical float offset in px, apply as a translateY. */
  floatY: number;
  /** Breathing scale multiplier, oscillates gently around 1. */
  breathScale: number;
  /** Natural micro gaze drift, small px offsets for the eyes/pupils. */
  gaze: Vec2;
}

/**
 * Drives slow, continuous idle motion (breathing float + wandering gaze)
 * using layered sine waves sampled on rAF. Runs independently of React
 * render cadence so it stays smooth even under load.
 */
export function useIdle({ enabled = true }: UseIdleOptions = {}): IdleState {
  const [state, setState] = useState<IdleState>({
    floatY: 0,
    breathScale: 1,
    gaze: { x: 0, y: 0 },
  });
  const rafRef = useRef<number>(0);
  const startRef = useRef<number>(performance.now());
  // Randomized per-mount so multiple faces on screen don't move in lockstep.
  const seedRef = useRef(Math.random() * 1000);

  useEffect(() => {
    if (!enabled) return;

    const loop = (t: number) => {
      const elapsed = (t - startRef.current) / 1000 + seedRef.current;

      const floatY = Math.sin(elapsed * 0.6) * 4;
      const breathScale = 1 + Math.sin(elapsed * 0.5) * 0.015;

      // Wandering gaze: two slow, slightly-detuned sine waves so the
      // path never quite repeats, kept within a small natural range.
      const gazeX = Math.sin(elapsed * 0.35) * 3 + Math.sin(elapsed * 0.13) * 1.5;
      const gazeY = Math.cos(elapsed * 0.27) * 2;

      setState({ floatY, breathScale, gaze: { x: gazeX, y: gazeY } });
      rafRef.current = requestAnimationFrame(loop);
    };

    rafRef.current = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(rafRef.current);
  }, [enabled]);

  return state;
}
