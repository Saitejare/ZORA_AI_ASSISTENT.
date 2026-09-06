import { useEffect, useRef } from 'react';

export const useVoiceWave = (
  canvasRef: React.RefObject<HTMLCanvasElement>,
  audioLevel: number,
  state: string,
) => {
  const phaseRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const width = canvas.width;
      const height = canvas.height;
      const centerY = height / 2;

      phaseRef.current += 0.05 + audioLevel * 0.1;

      let strokeColor = '#00f0ff';
      let secondaryColor = '#0066ff';

      if (state === 'Error') {
        strokeColor = '#ff5500';
        secondaryColor = '#ff0055';
      } else if (state === 'Recognizing') {
        strokeColor = '#7000ff';
        secondaryColor = '#00f0ff';
      }

      for (let waveIndex = 0; waveIndex < 3; waveIndex += 1) {
        ctx.beginPath();
        ctx.lineWidth = waveIndex === 0 ? 2.5 : 1.2;

        const alpha = 1 - waveIndex * 0.3;
        const freqMultiplier = 1 + waveIndex * 0.5;
        const ampMultiplier = (1 - waveIndex * 0.25) * (audioLevel * 40 + (state === 'Listening' ? 15 : 5));

        ctx.strokeStyle = waveIndex === 0 ? strokeColor : secondaryColor;
        ctx.globalAlpha = alpha;

        for (let x = 0; x < width; x += 2) {
          const normX = (x / width) * Math.PI * 2;
          const envelope = Math.sin((x / width) * Math.PI);
          let y = centerY;

          if (state === 'Recognizing') {
            y += Math.sin(Math.floor(x / 20) * 20 + phaseRef.current) * 10 * envelope;
          } else {
            y +=
              Math.sin(normX * freqMultiplier * 2 + phaseRef.current) *
              Math.cos(normX * 1.5 - phaseRef.current) *
              ampMultiplier *
              envelope;
          }

          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }

        ctx.stroke();
      }

      ctx.globalAlpha = 1;
      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => cancelAnimationFrame(animationFrameId);
  }, [canvasRef, audioLevel, state]);
};
