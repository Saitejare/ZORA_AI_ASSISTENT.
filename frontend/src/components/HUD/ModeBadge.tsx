import React from 'react';
import type { ZoraState } from '../../types';

interface ModeBadgeProps {
  state: ZoraState;
  onCycleState: () => void;
}

export const ModeBadge: React.FC<ModeBadgeProps> = React.memo(({ state, onCycleState }) => {
  const isError = state === 'Error';

  return (
    <button onClick={onCycleState} className={isError ? 'mode-badge mode-badge--error no-drag' : 'mode-badge no-drag'}>
      MODE: <span>{state}</span>
      <small>Click to Simulate</small>
    </button>
  );
});

ModeBadge.displayName = 'ModeBadge';
