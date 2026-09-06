import React from 'react';
import type { SystemStatus } from '../../types';

interface SystemStatsProps {
  stats: SystemStatus;
}

export const SystemStats: React.FC<SystemStatsProps> = React.memo(({ stats }) => (
  <div className="system-stats">
    <div>
      FPS: <span>{stats.fps}</span>
    </div>
    <div>
      CPU: <span>{stats.cpuUsage}%</span>
    </div>
    <div>
      RAM: <span>{stats.memoryUsage}%</span>
    </div>
  </div>
));

SystemStats.displayName = 'SystemStats';
