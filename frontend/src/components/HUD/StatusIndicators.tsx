import React from 'react';
import type { SystemStatus } from '../../types';

interface StatusIndicatorsProps {
  stats: SystemStatus;
}

const Indicator = ({ active, label, icon, variant = 'cyan' }: { active: boolean; label: string; icon: string; variant?: 'cyan' | 'purple' | 'emerald' }) => (
  <div className={`status-pill status-pill--${variant}`}>
    <span className={active ? 'status-pill__icon is-active' : 'status-pill__icon'}>{icon}</span>
    <span>{label}</span>
  </div>
);

export const StatusIndicators: React.FC<StatusIndicatorsProps> = React.memo(({ stats }) => (
  <div className="status-indicators no-drag">
    <Indicator active={stats.microphone} label="MIC" icon="M" />
    <Indicator active={stats.speaker} label="SPK" icon="S" />
    <Indicator active={stats.internet} label="NET" icon="W" />
    <Indicator active={stats.gpu} label="GPU" icon="C" variant="purple" />
    <Indicator active label="SECURE" icon="+" variant="emerald" />
  </div>
));

StatusIndicators.displayName = 'StatusIndicators';
