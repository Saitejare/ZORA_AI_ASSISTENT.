import React, { memo, useMemo } from 'react';
import { buildFaceMesh, buildHeadOutline, mixColor, type Triangle } from './faceGeometry';

interface FaceMeshProps {
  /** Tint blended into every facet, e.g. the accent or error color. */
  tintColor: string;
  /** 0..1 strength of the tint blend (rises for listening/speaking/thinking). */
  tintStrength: number;
}

const DARK_SHADE = '#0a1526';
const MID_SHADE = '#1c3a5e';
const LIGHT_SHADE = '#3f74ab';

// Computed once at module load - the silhouette/mesh never changes shape,
// only its per-facet color, so there is no reason to rebuild it per render.
const OUTLINE = buildHeadOutline();
const TRIANGLES: Triangle[] = buildFaceMesh(OUTLINE);

function pointsAttr(tri: Triangle) {
  return tri.points.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
}

// Each facet's base shade only depends on its fixed noise value, so it is
// computed once at module scope rather than on every render/tint change.
const FACET_BASE = TRIANGLES.map((tri, i) => ({
  key: i,
  points: pointsAttr(tri),
  shade:
    tri.noise < 0.5
      ? mixColor(DARK_SHADE, MID_SHADE, tri.noise * 2)
      : mixColor(MID_SHADE, LIGHT_SHADE, (tri.noise - 0.5) * 2),
}));

function rgbStringToHex(rgb: string): string {
  const match = rgb.match(/\d+/g);
  if (!match) return '#1c3a5e';
  const [r, g, b] = match.map(Number);
  return `#${[r, g, b].map((v) => v.toString(16).padStart(2, '0')).join('')}`;
}

/**
 * Renders the procedural low-poly mesh as SVG polygons. Each facet's base
 * shade is derived from its own deterministic noise value (so lighting
 * never flickers or re-randomizes), then blended toward `tintColor` by
 * `tintStrength` so the whole face washes warmer/brighter with state.
 */
function FaceMeshImpl({ tintColor, tintStrength }: FaceMeshProps) {
  const facets = useMemo(
    () =>
      FACET_BASE.map((f) => ({
        ...f,
        fill: mixColor(rgbStringToHex(f.shade), tintColor, tintStrength),
      })),
    [tintColor, tintStrength],
  );

  return (
    <g>
      {facets.map((f) => (
        <polygon
          key={f.key}
          points={f.points}
          fill={f.fill}
          stroke="rgba(190, 220, 255, 0.08)"
          strokeWidth={0.6}
          style={{ transition: 'fill 0.4s ease' }}
        />
      ))}
    </g>
  );
}

export const FaceMesh = memo(FaceMeshImpl);
export default FaceMesh;
