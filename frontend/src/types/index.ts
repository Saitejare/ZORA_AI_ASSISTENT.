export type ZoraState =
  | 'Idle'
  | 'Listening'
  | 'Recognizing'
  | 'Thinking'
  | 'Speaking'
  | 'Searching'
  | 'Executing'
  | 'Happy'
  | 'Error'
  | 'Sleeping';

export interface SystemStatus {
  microphone: boolean;
  speaker: boolean;
  internet: boolean;
  gpu: boolean;
  fps: number;
  cpuUsage: number;
  memoryUsage: number;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
  timestamp: string;
}
