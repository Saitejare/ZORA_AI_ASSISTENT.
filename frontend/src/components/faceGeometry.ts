import type { Vec2 } from '../types/FaceState';
import { delaunayTriangulate } from './delaunay';

/**
 * Procedural face geometry.
 *
 * Instead of hand-authoring hundreds of triangles, we describe the head
 * silhouette as a small number of (y, halfWidth) keyframes, spline them into
 * a smooth outline, then radially triangulate the interior into a low-poly
 * mesh (concentric, slightly-jittered "rings" stitched together) - the same
 * family of technique used to produce the low-poly "digital face" look.
 */

export interface Triangle {
  points: [Vec2, Vec2, Vec2];
  /** Deterministic 0..1 pseudo-random value used to vary facet shading. */
  noise: number;
}

// [y, halfWidth] keyframes from the crown of the head down to the chin tip.
const PROFILE: Array<[number, number]> = [
  [-150, 6],
  [-138, 40],
  [-118, 58],
  [-95, 70],
  [-60, 75],
  [-20, 76],
  [20, 72],
  [55, 62],
  [85, 46],
  [108, 28],
  [125, 10],
  [134, 0],
];

function catmullRom(p0: number, p1: number, p2: number, p3: number, t: number) {
  const t2 = t * t;
  const t3 = t2 * t;
  return 0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3);
}

/** Builds a smooth, closed head silhouette (right side, then mirrored left side). */
export function buildHeadOutline(samplesPerSegment = 3): Vec2[] {
  const ys = PROFILE.map((p) => p[0]);
  const ws = PROFILE.map((p) => p[1]);
  const right: Vec2[] = [];

  for (let i = 0; i < PROFILE.length - 1; i++) {
    const i0 = Math.max(0, i - 1);
    const i3 = Math.min(ys.length - 1, i + 2);
    for (let s = 0; s < samplesPerSegment; s++) {
      const t = s / samplesPerSegment;
      const y = catmullRom(ys[i0], ys[i], ys[i + 1], ys[i3], t);
      const w = catmullRom(ws[i0], ws[i], ws[i + 1], ws[i3], t);
      right.push({ x: w, y });
    }
  }
  right.push({ x: ws[ws.length - 1], y: ys[ys.length - 1] });

  const left = [...right].reverse().map((p) => ({ x: -p.x, y: p.y }));
  return [...right, ...left];
}

/** Deterministic 2D hash -> [0, 1), used so facet shading never re-randomizes on re-render. */
export function hash2(x: number, y: number): number {
  const s = Math.sin(x * 12.9898 + y * 78.233) * 43758.5453;
  return s - Math.floor(s);
}

function lerp(a: Vec2, b: Vec2, t: number): Vec2 {
  return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
}

const FACE_CENTER: Vec2 = { x: 0, y: -6 };
const MAX_RADIUS = 132;

function makeTriangle(a: Vec2, b: Vec2, c: Vec2): Triangle {
  const cx = (a.x + b.x + c.x) / 3;
  const cy = (a.y + b.y + c.y) / 3;
  const dist = Math.hypot(cx - FACE_CENTER.x, cy - FACE_CENTER.y);
  const centerBrightness = 1 - Math.min(1, dist / MAX_RADIUS);
  const grain = hash2(cx * 0.6, cy * 0.6);
  const shade = Math.max(0, Math.min(1, centerBrightness * 0.72 + grain * 0.42 - 0.06));
  return { points: [a, b, c], noise: shade };
}

/** Standard ray-casting point-in-polygon test. */
function pointInPolygon(pt: Vec2, poly: Vec2[]): boolean {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i].x;
    const yi = poly[i].y;
    const xj = poly[j].x;
    const yj = poly[j].y;
    const intersects = yi > pt.y !== yj > pt.y && pt.x < ((xj - xi) * (pt.y - yi)) / (yj - yi) + xi;
    if (intersects) inside = !inside;
  }
  return inside;
}

/**
 * Scatters a jittered grid of interior points across the outline's bounding
 * box, keeping only the ones that actually fall inside the silhouette.
 */
function scatterInteriorPoints(outline: Vec2[], gridStep: number): Vec2[] {
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (const p of outline) {
    if (p.x < minX) minX = p.x;
    if (p.y < minY) minY = p.y;
    if (p.x > maxX) maxX = p.x;
    if (p.y > maxY) maxY = p.y;
  }

  const points: Vec2[] = [];
  for (let x = minX; x <= maxX; x += gridStep) {
    for (let y = minY; y <= maxY; y += gridStep) {
      const jitterX = (hash2(x * 0.11, y * 0.37) - 0.5) * gridStep * 0.85;
      const jitterY = (hash2(x * 0.29, y * 0.13) - 0.5) * gridStep * 0.85;
      const p = { x: x + jitterX, y: y + jitterY };
      if (pointInPolygon(p, outline)) points.push(p);
    }
  }
  return points;
}

/**
 * Builds an organic low-poly face mesh: the head silhouette's own outline
 * points plus a jittered scatter of interior points, Delaunay-triangulated,
 * then trimmed to triangles whose centroid actually falls inside the
 * silhouette (discarding any hull artifacts around concave regions like
 * the chin taper).
 */
export function buildFaceMesh(outline: Vec2[], gridStep = 13): Triangle[] {
  const interior = scatterInteriorPoints(outline, gridStep);
  const allPoints = [...outline, ...interior];
  const indexTriangles = delaunayTriangulate(allPoints);

  const triangles: Triangle[] = [];
  for (const t of indexTriangles) {
    const a = allPoints[t.a];
    const b = allPoints[t.b];
    const c = allPoints[t.c];
    const centroid = { x: (a.x + b.x + c.x) / 3, y: (a.y + b.y + c.y) / 3 };
    if (!pointInPolygon(centroid, outline)) continue;
    triangles.push(makeTriangle(a, b, c));
  }
  return triangles;
}

/** Named bone-landmark points, positioned like the glowing nodes in a face-scan mesh. */
export const LANDMARKS: Record<string, Vec2> = {
  crownLeft: { x: -22, y: -128 },
  crownRight: { x: 22, y: -128 },
  templeLeft: { x: -66, y: -95 },
  templeRight: { x: 66, y: -95 },
  foreheadCenter: { x: 0, y: -78 },
  browRidgeLeft: { x: -46, y: -18 },
  browRidgeRight: { x: 46, y: -18 },
  noseBridge: { x: 0, y: -6 },
  cheekLeft: { x: -58, y: 14 },
  cheekRight: { x: 58, y: 14 },
  noseAlaLeft: { x: -16, y: 34 },
  noseAlaRight: { x: 16, y: 34 },
  philtrum: { x: 0, y: 58 },
  jawLeft: { x: -46, y: 96 },
  jawRight: { x: 46, y: 96 },
  chin: { x: 0, y: 124 },
};

/** Edges (by landmark name) drawn as the faint connective "constellation" lines. */
export const LANDMARK_EDGES: Array<[string, string]> = [
  ['crownLeft', 'crownRight'],
  ['crownLeft', 'templeLeft'],
  ['crownRight', 'templeRight'],
  ['crownLeft', 'foreheadCenter'],
  ['crownRight', 'foreheadCenter'],
  ['templeLeft', 'browRidgeLeft'],
  ['templeRight', 'browRidgeRight'],
  ['foreheadCenter', 'noseBridge'],
  ['browRidgeLeft', 'noseBridge'],
  ['browRidgeRight', 'noseBridge'],
  ['browRidgeLeft', 'cheekLeft'],
  ['browRidgeRight', 'cheekRight'],
  ['templeLeft', 'cheekLeft'],
  ['templeRight', 'cheekRight'],
  ['noseBridge', 'noseAlaLeft'],
  ['noseBridge', 'noseAlaRight'],
  ['cheekLeft', 'noseAlaLeft'],
  ['cheekRight', 'noseAlaRight'],
  ['noseAlaLeft', 'philtrum'],
  ['noseAlaRight', 'philtrum'],
  ['cheekLeft', 'jawLeft'],
  ['cheekRight', 'jawRight'],
  ['philtrum', 'chin'],
  ['jawLeft', 'chin'],
  ['jawRight', 'chin'],
];

function hexToRgb(hex: string) {
  const clean = hex.replace('#', '');
  const full = clean.length === 3 ? clean.split('').map((c) => c + c).join('') : clean;
  const value = parseInt(full, 16);
  return { r: (value >> 16) & 255, g: (value >> 8) & 255, b: value & 255 };
}

/** Linearly mixes two hex colors, returning an `rgb()` string. */
export function mixColor(hexA: string, hexB: string, t: number): string {
  const a = hexToRgb(hexA);
  const b = hexToRgb(hexB);
  const clampedT = Math.max(0, Math.min(1, t));
  const r = Math.round(a.r + (b.r - a.r) * clampedT);
  const g = Math.round(a.g + (b.g - a.g) * clampedT);
  const bch = Math.round(a.b + (b.b - a.b) * clampedT);
  return `rgb(${r}, ${g}, ${bch})`;
}
