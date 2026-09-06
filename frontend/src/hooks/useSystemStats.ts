import { useEffect, useRef, useState } from 'react';
import type { SystemStatus } from '../types';

export const useSystemStats = (): SystemStatus => {
  const frameRequestRef = useRef<number>();
  const [stats, setStats] = useState<SystemStatus>({
    microphone: true,
    speaker: true,
    internet: true,
    gpu: true,
    fps: 60,
    cpuUsage: 12,
    memoryUsage: 34,
  });

  useEffect(() => {
    let lastTime = performance.now();
    let frameCount = 0;

    const interval = setInterval(() => {
      const now = performance.now();
      const delta = (now - lastTime) / 1000;
      const currentFps = Math.round(frameCount / delta);

      frameCount = 0;
      lastTime = now;

      setStats((prev) => ({
        ...prev,
        fps: Math.min(60, currentFps || 60),
        cpuUsage: Math.floor(10 + Math.random() * 15),
        memoryUsage: Math.floor(32 + Math.random() * 5),
      }));
    }, 2000);

    const countFrames = () => {
      frameCount += 1;
      frameRequestRef.current = requestAnimationFrame(countFrames);
    };

    frameRequestRef.current = requestAnimationFrame(countFrames);

    return () => {
      clearInterval(interval);
      if (frameRequestRef.current) cancelAnimationFrame(frameRequestRef.current);
    };
  }, []);

  return stats;
};
