import React, { memo, useEffect, useRef } from 'react';

interface ParticlesProps {
  /** Ramps particle speed/brightness up (used for the listening state). */
  active?: boolean;
  /** Base accent color for particle glow. */
  color?: string;
  /** Number of particles to simulate. */
  count?: number;
  className?: string;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  r: number;
  baseAlpha: number;
  twinklePhase: number;
}

/**
 * Lightweight HTML5 Canvas particle field drawn behind the face.
 * Runs its own rAF loop and resizes with the container via ResizeObserver,
 * so it stays crisp and responsive without triggering React re-renders.
 */
function ParticlesImpl({ active = false, color = '#4da8ff', count = 60, className }: ParticlesProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const particlesRef = useRef<Particle[]>([]);
  const activeRef = useRef(active);
  const rafRef = useRef<number>(0);
  const dprRef = useRef(1);

  activeRef.current = active;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const initParticles = (width: number, height: number) => {
      particlesRef.current = Array.from({ length: count }, () => ({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.15,
        vy: (Math.random() - 0.5) * 0.15,
        r: Math.random() * 1.6 + 0.4,
        baseAlpha: Math.random() * 0.5 + 0.15,
        twinklePhase: Math.random() * Math.PI * 2,
      }));
    };

    const resize = () => {
      const parent = canvas.parentElement;
      if (!parent) return;
      const { width, height } = parent.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      dprRef.current = dpr;
      canvas.width = Math.max(1, Math.floor(width * dpr));
      canvas.height = Math.max(1, Math.floor(height * dpr));
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      initParticles(width, height);
    };

    resize();
    const ro = new ResizeObserver(resize);
    if (canvas.parentElement) ro.observe(canvas.parentElement);

    let frame = 0;
    const draw = () => {
      frame += 1;
      const dpr = dprRef.current;
      const width = canvas.width / dpr;
      const height = canvas.height / dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, width, height);

      const speedMul = activeRef.current ? 2.6 : 1;
      const alphaMul = activeRef.current ? 1.6 : 1;

      for (const p of particlesRef.current) {
        p.x += p.vx * speedMul;
        p.y += p.vy * speedMul;

        if (p.x < 0) p.x = width;
        if (p.x > width) p.x = 0;
        if (p.y < 0) p.y = height;
        if (p.y > height) p.y = 0;

        const twinkle = 0.5 + 0.5 * Math.sin(frame * 0.02 + p.twinklePhase);
        const alpha = Math.min(1, p.baseAlpha * twinkle * alphaMul);

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * (activeRef.current ? 1.3 : 1), 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.globalAlpha = alpha;
        ctx.fill();
      }
      ctx.globalAlpha = 1;

      rafRef.current = requestAnimationFrame(draw);
    };

    rafRef.current = requestAnimationFrame(draw);

    return () => {
      cancelAnimationFrame(rafRef.current);
      ro.disconnect();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [count, color]);

  return <canvas ref={canvasRef} className={className} aria-hidden="true" />;
}

export const Particles = memo(ParticlesImpl);
export default Particles;
