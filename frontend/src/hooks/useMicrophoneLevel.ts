import { useCallback, useEffect, useRef, useState } from 'react';

interface MicrophoneLevel {
  audioLevel: number;
  isActive: boolean;
  error: string | null;
  start: () => Promise<void>;
  stop: () => void;
}

export const useMicrophoneLevel = (): MicrophoneLevel => {
  const [audioLevel, setAudioLevel] = useState(0);
  const [isActive, setIsActive] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const animationFrameRef = useRef<number>();

  const stop = useCallback(() => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = undefined;
    }

    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
    void audioContextRef.current?.close();
    audioContextRef.current = null;
    analyserRef.current = null;
    setAudioLevel(0);
    setIsActive(false);
  }, []);

  const start = useCallback(async () => {
    try {
      setError(null);
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });

      const audioContext = new AudioContext();
      const analyser = audioContext.createAnalyser();
      const source = audioContext.createMediaStreamSource(stream);

      analyser.fftSize = 1024;
      analyser.smoothingTimeConstant = 0.72;
      source.connect(analyser);

      streamRef.current = stream;
      audioContextRef.current = audioContext;
      analyserRef.current = analyser;
      setIsActive(true);

      const samples = new Uint8Array(analyser.frequencyBinCount);

      const updateLevel = () => {
        analyser.getByteTimeDomainData(samples);

        let sumSquares = 0;
        for (const sample of samples) {
          const normalized = (sample - 128) / 128;
          sumSquares += normalized * normalized;
        }

        const rms = Math.sqrt(sumSquares / samples.length);
        const boostedLevel = Math.min(1, Math.max(0, (rms - 0.015) * 8));
        setAudioLevel(boostedLevel);
        animationFrameRef.current = requestAnimationFrame(updateLevel);
      };

      updateLevel();
    } catch {
      stop();
      setError('Microphone permission unavailable');
    }
  }, [stop]);

  useEffect(() => stop, [stop]);

  return { audioLevel, isActive, error, start, stop };
};
