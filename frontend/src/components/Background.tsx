import React, { memo, type ReactNode } from 'react';
import Particles from './Particles';

interface BackgroundProps {
  active?: boolean;
  accentColor?: string;
  transparent?: boolean;
  children?: ReactNode;
}

/**
 * Responsive container behind the face: an optional subtle grid + vignette
 * (skipped entirely when `transparent` is set, e.g. embedding over a host
 * app's own background) plus the ambient particle canvas.
 */
function BackgroundImpl({ active = false, accentColor = '#4da8ff', transparent = false, children }: BackgroundProps) {
  return (
    <div className={`aiface-background ${transparent ? 'aiface-background--transparent' : ''}`}>
      {!transparent && <div className="aiface-background__grid" aria-hidden="true" />}
      {!transparent && <div className="aiface-background__vignette" aria-hidden="true" />}
      <Particles active={active} color={accentColor} className="aiface-background__particles" />
      <div className="aiface-background__content">{children}</div>
    </div>
  );
}

export const Background = memo(BackgroundImpl);
export default Background;
