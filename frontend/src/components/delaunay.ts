import type { Vec2 } from '../types/FaceState';

/**
 * Minimal Bowyer-Watson Delaunay triangulation. Pure TypeScript, no
 * external geometry library - keeps the project dependency-free per the
 * project constraints (React + TS + SVG + Canvas + CSS + Framer Motion
 * only). Fine for the couple hundred points a face mesh needs.
 */

interface IndexTriangle {
  a: number;
  b: number;
  c: number;
}

function circumcircle(p1: Vec2, p2: Vec2, p3: Vec2) {
  const { x: ax, y: ay } = p1;
  const { x: bx, y: by } = p2;
  const { x: cx, y: cy } = p3;
  const d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by));
  if (Math.abs(d) < 1e-9) return null;

  const aSq = ax * ax + ay * ay;
  const bSq = bx * bx + by * by;
  const cSq = cx * cx + cy * cy;

  const ux = (aSq * (by - cy) + bSq * (cy - ay) + cSq * (ay - by)) / d;
  const uy = (aSq * (cx - bx) + bSq * (ax - cx) + cSq * (bx - ax)) / d;
  const r2 = (ax - ux) ** 2 + (ay - uy) ** 2;
  return { x: ux, y: uy, r2 };
}

function edgeKey(a: number, b: number) {
  return a < b ? `${a}_${b}` : `${b}_${a}`;
}

/** Returns triangles as index triples into the input `points` array. */
export function delaunayTriangulate(points: Vec2[]): IndexTriangle[] {
  const n = points.length;
  if (n < 3) return [];

  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;
  for (const p of points) {
    if (p.x < minX) minX = p.x;
    if (p.y < minY) minY = p.y;
    if (p.x > maxX) maxX = p.x;
    if (p.y > maxY) maxY = p.y;
  }
  const deltaMax = Math.max(maxX - minX, maxY - minY) * 20;
  const midX = (minX + maxX) / 2;
  const midY = (minY + maxY) / 2;

  // Super-triangle large enough to contain every input point.
  const superPoints: Vec2[] = [
    { x: midX - deltaMax, y: midY - deltaMax },
    { x: midX, y: midY + deltaMax },
    { x: midX + deltaMax, y: midY - deltaMax },
  ];
  const pts = [...points, ...superPoints];
  const superIdx = [n, n + 1, n + 2];

  let triangles: IndexTriangle[] = [{ a: superIdx[0], b: superIdx[1], c: superIdx[2] }];

  for (let i = 0; i < n; i++) {
    const p = pts[i];
    const bad: IndexTriangle[] = [];
    for (const t of triangles) {
      const cc = circumcircle(pts[t.a], pts[t.b], pts[t.c]);
      if (!cc) continue;
      const dx = p.x - cc.x;
      const dy = p.y - cc.y;
      if (dx * dx + dy * dy <= cc.r2) bad.push(t);
    }

    const edgeCount = new Map<string, { a: number; b: number; count: number }>();
    for (const t of bad) {
      const edges: Array<[number, number]> = [
        [t.a, t.b],
        [t.b, t.c],
        [t.c, t.a],
      ];
      for (const [a, b] of edges) {
        const key = edgeKey(a, b);
        const existing = edgeCount.get(key);
        if (existing) existing.count += 1;
        else edgeCount.set(key, { a, b, count: 1 });
      }
    }

    const badSet = new Set(bad);
    triangles = triangles.filter((t) => !badSet.has(t));
    for (const { a, b, count } of edgeCount.values()) {
      if (count === 1) triangles.push({ a, b, c: i });
    }
  }

  // Drop any triangle touching a super-triangle vertex.
  return triangles.filter((t) => t.a < n && t.b < n && t.c < n);
}
