import React, { useEffect, useState } from 'react';

export const TopNav: React.FC = React.memo(() => {
  const [timeStr, setTimeStr] = useState('');
  const [dateStr, setDateStr] = useState('');

  useEffect(() => {
    const updateDateTime = () => {
      const now = new Date();
      setTimeStr(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }));
      setDateStr(now.toLocaleDateString([], { weekday: 'short', month: 'short', day: '2-digit', year: 'numeric' }).toUpperCase());
    };

    updateDateTime();
    const interval = setInterval(updateDateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="top-nav drag-region">
      <h1>
        ZORA <span>v2.5 ARCHITECT</span>
      </h1>
      <div className="top-nav__meta">
        <span>{timeStr}</span>
        <span className="top-nav__divider">|</span>
        <span>{dateStr}</span>
      </div>
    </div>
  );
});

TopNav.displayName = 'TopNav';
