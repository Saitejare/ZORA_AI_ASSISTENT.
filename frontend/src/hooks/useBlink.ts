import { useEffect, useState } from 'react';

type BlinkOptions = {
  enabled?: boolean;
};

export function useBlink(state: string): boolean;
export function useBlink(options: BlinkOptions): { isBlinking: boolean };
export function useBlink(input: string | BlinkOptions) {
  const state = typeof input === 'string' ? input : input.enabled === false ? 'Sleeping' : 'Idle';
  const [isBlinking, setIsBlinking] = useState(false);

  useEffect(() => {
    if (state === 'Sleeping') {
      setIsBlinking(true);
      return;
    }

    let timer: ReturnType<typeof setTimeout>;

    const scheduleBlink = () => {
      const nextInterval = Math.random() * 3000 + 3000;
      timer = setTimeout(() => {
        setIsBlinking(true);
        setTimeout(() => {
          setIsBlinking(false);
          scheduleBlink();
        }, 150);
      }, nextInterval);
    };

    scheduleBlink();

    return () => clearTimeout(timer);
  }, [state]);

  return typeof input === 'string' ? isBlinking : { isBlinking };
}
