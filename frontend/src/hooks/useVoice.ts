import { useEffect, useRef, useState } from 'react';

interface UseVoiceOptions {
  /** Raw, possibly-jittery audio amplitude, 0..1. */
  audioLevel: number;
  isSpeaking: boolean;
  /** Higher = snappier response, lower = smoother/slower. */
  smoothing?: number;
}

/**
 * Smooths a raw audioLevel value on every animation frame using
 * exponential interpolation, so the mouth never "jumps" between frames.
 * Falls back to a gentle idle murmur curve when not speaking.
 */
export function useVoice({ audioLevel, isSpeaking, smoothing = 0.18 }: UseVoiceOptions) {
  const [smoothLevel, setSmoothLevel] = useState(0);
  const rafRef = useRef<number>(0);
  const currentRef = useRef(0);
  const targetRef = useRef(0);

  // Keep the target in a ref so the rAF loop always reads the latest value
  // without needing to be re-created every prop change.
  targetRef.current = isSpeaking ? Math.max(0, Math.min(1, audioLevel)) : 0;

  useEffect(() => {
    const tick = () => {
      const current = currentRef.current;
      const target = targetRef.current;
      const next = current + (target - current) * smoothing;
      currentRef.current = Math.abs(next - target) < 0.001 ? target : next;
      setSmoothLevel(currentRef.current);
      rafRef.current = requestAnimationFrame(tick);
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [smoothing]);

  return { mouthOpenness: smoothLevel };
}
