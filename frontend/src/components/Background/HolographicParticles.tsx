import React, { useEffect, useRef } from 'react';
import { useParticles } from '../../hooks/useParticles';

interface HolographicParticlesProps {
  state: string;
}

export const HolographicParticles: React.FC<HolographicParticlesProps> = React.memo(({ state }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const handleResize = () => {
      if (canvasRef.current) {
        canvasRef.current.width = window.innerWidth;
        canvasRef.current.height = window.innerHeight;
      }
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useParticles(canvasRef, state);

  return <canvas ref={canvasRef} className="zora-particles scanlines" />;
});

HolographicParticles.displayName = 'HolographicParticles';
