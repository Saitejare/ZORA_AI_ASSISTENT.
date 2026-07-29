# BERU — Holographic AI Assistant Face

A minimal, futuristic holographic AI face component built with **React + TypeScript + SVG + HTML5 Canvas + CSS + Framer Motion only**. No Three.js, no Blender/Live2D/VRM exports, no images, no Lottie — every visual is generated procedurally in the browser.

The component defaults to the name **BERU** (used in its accessible `aria-label`), but this is fully overridable via the `name` prop shown below.

## Quick start

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build in dist/
```

The `dist/` output is static HTML/CSS/JS and can be loaded directly inside an Electron `BrowserWindow` (relative asset paths are already configured in `vite.config.ts`).

## Using the component

```tsx
import AIFace from './components/AIFace';

<AIFace
  isSpeaking={false}
  isListening={false}
  isThinking={false}
  emotion="neutral"     // 'neutral' | 'happy' | 'error'
  audioLevel={0}        // 0..1, drives mouth openness while speaking
  volume={0}            // 0..1, boosts the glow while speaking
  isSleeping={false}
  accentColor="#5eead4" // optional, defaults to a cyan holographic accent
  size="100%"           // optional, any CSS size; the face stays square & responsive
  name="BERU"           // optional, accessible name announced via aria-label
/>
```

Only one "mode" is ever visually active at a time; if multiple booleans are
true simultaneously, `AIFace` resolves them with this priority:

```
isSleeping > emotion === 'error' > isSpeaking > isListening > isThinking > emotion === 'happy' > idle
```

## Architecture

```
src/
  components/
    AIFace.tsx      – public entry point, resolves props -> mode, wires up hooks
    Head.tsx         – head outline, forehead, brows, nose, jaw/chin, orbit dots, halo
    Eyes.tsx         – positions the eye pair, resolves gaze/color/brightness per mode
    Eye.tsx          – single eye: outline, iris, pupil, animated eyelid
    Mouth.tsx        – lip path generator, interpolates open/width from audioLevel
    Glow.tsx         – layered blurred radial-gradient bloom behind the head
    Particles.tsx    – <canvas> ambient particle field, boosts on `active`
    Background.tsx   – responsive wrapper: grid + vignette + particles + content
    Animations.ts    – shared Framer Motion variants/transitions/presets
  hooks/
    useBlink.ts      – random 3-6s blink scheduling
    useVoice.ts       – rAF-smoothed audioLevel -> mouthOpenness
    useIdle.ts       – rAF-driven float / breathing / gaze-drift sine waves
    useThinking.ts   – rAF-driven rotation angle for the orbiting "thinking" dots
  types/
    FaceState.ts     – AIFaceProps, FaceMode, Emotion, Vec2
  styles/
    aiface.css       – responsive layout, glow, dark-mode & transparency support
```

## Animation states

| State      | Behavior |
|------------|----------|
| Idle       | Slow breathing glow, gentle float, wandering gaze, ambient particles |
| Blink      | Random interval every 3-6s, ~160ms eyelid close/open |
| Speaking   | Mouth width/height driven by `audioLevel` (0 closed → 1 max open), glow rises with `volume`, chin shifts slightly, gaze locks forward |
| Listening  | Eyes brighten, pulsing halo ring around the head, particles speed up |
| Thinking   | Gaze glances slightly upward, glow pulses, three dots orbit the head |
| Happy      | Corners of the mouth lift into a small smile, eyes soften (squint) |
| Error      | Eyes and outline shift to orange, glow dims |
| Sleeping   | Eyes fully closed, only the breathing loop keeps running |

## Performance notes

- All continuous motion (`useIdle`, `useVoice`, `useThinking`) runs its own
  `requestAnimationFrame` loop decoupled from React's render cycle; only the
  minimal derived numbers are pushed into state/refs consumed by memoized
  components (`React.memo` on every component in `components/`).
- Every animated CSS/SVG property is `transform`/`opacity` (translate, scale,
  rotate, fill/stroke color, opacity) so the browser can composite on the
  GPU without triggering layout or paint of the whole tree.
- `Particles` draws to a single `<canvas>` sized via `ResizeObserver` and a
  capped device pixel ratio (max 2), rather than re-rendering DOM nodes per
  particle.
- `prefers-reduced-motion` is respected: ambient loops are disabled while
  state-change transitions remain.

## Electron / transparent background

`Background` accepts a `transparent` flag (wire it through if you need it)
that skips the opaque grid/vignette so the face can sit directly on a host
window's own background — useful for an always-on-top Electron overlay.
