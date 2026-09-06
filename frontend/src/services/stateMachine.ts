import type { ZoraState } from '../types';

export const ALL_STATES: ZoraState[] = [
  'Idle',
  'Listening',
  'Recognizing',
  'Thinking',
  'Speaking',
  'Searching',
  'Executing',
  'Happy',
  'Error',
  'Sleeping',
];

export const getNextState = (currentState: ZoraState): ZoraState => {
  const currentIndex = ALL_STATES.indexOf(currentState);
  const nextIndex = (currentIndex + 1) % ALL_STATES.length;
  return ALL_STATES[nextIndex];
};
