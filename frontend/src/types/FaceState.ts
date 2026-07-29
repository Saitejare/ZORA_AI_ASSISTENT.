/**
 * Shared type definitions for the AI holographic face system.
 */

/** High level emotional expression of the assistant. */
export type Emotion = 'neutral' | 'happy' | 'error';

/** The resolved, mutually-exclusive "mode" the face is currently in. */
export type FaceMode =
  | 'sleeping'
  | 'error'
  | 'speaking'
  | 'listening'
  | 'thinking'
  | 'happy'
  | 'idle';

/** Public props accepted by <AIFace />. */
export interface AIFaceProps {
  /** Mouth should animate open/closed driven by audioLevel. */
  isSpeaking?: boolean;
  /** Eyes brighten + halo pulse appears around the head. */
  isListening?: boolean;
  /** Eyes glance up, orbiting dots appear, glow pulses slowly. */
  isThinking?: boolean;
  /** Named emotional expression layered on top of the current mode. */
  emotion?: Emotion;
  /** Instantaneous audio amplitude in the 0..1 range, drives mouth shape. */
  audioLevel?: number;
  /** Overall output volume in the 0..1 range, scales glow intensity. */
  volume?: number;
  /** Puts the face into a low-power, eyes-closed breathing state. */
  isSleeping?: boolean;
  /** Optional accent color override (defaults to cyan holographic accent). */
  accentColor?: string;
  /** Optional pixel size; the face is a responsive square that fills its container by default. */
  size?: number | string;
  /** Extra class name for the outer wrapper. */
  className?: string;
  /** Display/accessible name for the assistant (used in aria-label). Defaults to "BERU". */
  name?: string;
}

/** Normalized internal state derived from props, consumed by child components. */
export interface DerivedFaceState {
  mode: FaceMode;
  emotion: Emotion;
  audioLevel: number;
  volume: number;
  accentColor: string;
}

/** Simple 2D point, used for gaze / drift offsets. */
export interface Vec2 {
  x: number;
  y: number;
}
