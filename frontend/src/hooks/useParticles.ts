import { useEffect, useRef } from 'react';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
  alpha: number;
  pulseSpeed: number;
}

export const useParticles = (canvasRef: React.RefObject<HTMLCanvasElement>, state: string) => {
  const particlesRef = useRef<Particle[]>([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    particlesRef.current = Array.from({ length: 120 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.5,
      vy: (Math.random() - 0.5) * 0.5,
      size: Math.random() * 2 + 0.5,
      alpha: Math.random() * 0.7 + 0.2,
      pulseSpeed: Math.random() * 0.02 + 0.005,
    }));

    let animationFrameId: number;

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      let speedFactor = 1;
      let particleColor = '0, 240, 255';

      if (state === 'Listening' || state === 'Searching') {
        speedFactor = 2.5;
      } else if (state === 'Thinking' || state === 'Executing') {
        speedFactor = 1.8;
        particleColor = '112, 0, 255';
      } else if (state === 'Error') {
        particleColor = '255, 85, 0';
      } else if (state === 'Sleeping') {
        speedFactor = 0.3;
      }

      particlesRef.current.forEach((p, index) => {
        p.x += p.vx * speedFactor;
        p.y += p.vy * speedFactor;

        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;

        p.alpha += Math.sin(Date.now() * p.pulseSpeed) * 0.01;
        const clampedAlpha = Math.max(0.1, Math.min(0.8, p.alpha));

        ctx.fillStyle = `rgba(${particleColor}, ${clampedAlpha})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();

        for (let i = index + 1; i < particlesRef.current.length; i += 1) {
          const p2 = particlesRef.current[i];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 80) {
            ctx.strokeStyle = `rgba(${particleColor}, ${0.15 * (1 - dist / 80)})`;
            ctx.lineWidth = 0.5;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
          }
        }
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => cancelAnimationFrame(animationFrameId);
  }, [canvasRef, state]);
};
