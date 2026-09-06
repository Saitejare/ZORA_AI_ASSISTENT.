import React from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import type { NotificationItem } from '../../types';

interface NotificationStackProps {
  notifications: NotificationItem[];
}

const iconByType: Record<NotificationItem['type'], string> = {
  info: 'i',
  success: '+',
  warning: '!',
  error: 'x',
};

export const NotificationStack: React.FC<NotificationStackProps> = React.memo(({ notifications }) => (
  <div className="notification-stack">
    <AnimatePresence>
      {notifications.map((notification) => (
        <motion.div
          key={notification.id}
          initial={{ opacity: 0, x: 50, scale: 0.9 }}
          animate={{ opacity: 1, x: 0, scale: 1 }}
          exit={{ opacity: 0, x: 20, scale: 0.95 }}
          transition={{ duration: 0.25 }}
          className={`notification notification--${notification.type}`}
        >
          <span className="notification__icon">{iconByType[notification.type]}</span>
          <div>
            <span className="notification__title">{notification.title}</span>
            <span className="notification__message">{notification.message}</span>
            <span className="notification__timestamp">{notification.timestamp}</span>
          </div>
        </motion.div>
      ))}
    </AnimatePresence>
  </div>
));

NotificationStack.displayName = 'NotificationStack';
