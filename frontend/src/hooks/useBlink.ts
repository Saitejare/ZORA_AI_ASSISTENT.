import { useEffect, useRef, useState } from 'react';

interface UseBlinkOptions {
  /** Blinking is suspended while asleep (eyes are already closed) or in error state. */
  enabled?: boolean;
  minDelayMs?: number;
  maxDelayMs?: number;
  blinkDurationMs?: number;
}

/**
 * Schedules a natural blink on a random interval (default 3-6s).
 * Returns `isBlinking`, a transient boolean that stays true only for the
 * duration of the eyelid close/open animation.
 */
export function useBlink({
  enabled = true,
  minDelayMs = 3000,
  maxDelayMs = 6000,
  blinkDurationMs = 160,
}: UseBlinkOptions = {}) {
  const [isBlinking, setIsBlinking] = useState(false);
  const timeoutRef = useRef<number | null>(null);
  const blinkTimeoutRef = useRef<number | null>(null);

  useEffect(() => {
    if (!enabled) {
      setIsBlinking(false);
      return;
    }

    const scheduleNext = () => {
      const delay = minDelayMs + Math.random() * (maxDelayMs - minDelayMs);
      timeoutRef.current = window.setTimeout(() => {
        setIsBlinking(true);
        blinkTimeoutRef.current = window.setTimeout(() => {
          setIsBlinking(false);
          scheduleNext();
        }, blinkDurationMs);
      }, delay);
    };

    scheduleNext();

    return () => {
      if (timeoutRef.current) window.clearTimeout(timeoutRef.current);
      if (blinkTimeoutRef.current) window.clearTimeout(blinkTimeoutRef.current);
    };
  }, [enabled, minDelayMs, maxDelayMs, blinkDurationMs]);

  return { isBlinking };
}
