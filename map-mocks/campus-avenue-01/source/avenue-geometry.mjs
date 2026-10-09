/** Original arrival garden. All geometry is native pixels; the avatar frame remains 32×32. */
export const AVENUE = Object.freeze({
  id: 'magical-universe-arrival-avenue',
  nativeSize: { width: 1472, height: 576 },
  tileSize: 32,
  worldOrigin: { x: 704, y: 2480 },
  arrival: { x: 800, y: 432 },
  avatar: { frame: { x: -16, y: -16, width: 32, height: 32 }, body: { x: -8, y: 0, width: 16, height: 16 }, scale: 1 },
  walkable: [
    [[736, 0], [864, 0], [864, 576], [736, 576]],
    [[0, 256], [800, 256], [800, 352], [0, 352]]
  ],
  obstacles: [
    { id: 'northwest-garden', type: 'rect', x: 0, y: 0, width: 736, height: 256 },
    { id: 'southwest-garden', type: 'rect', x: 0, y: 352, width: 736, height: 224 },
    { id: 'east-garden', type: 'rect', x: 864, y: 0, width: 608, height: 576 }
  ],
  receivers: {
    north: { edge: 'north', center: 800, from: 736, to: 864, clearWidth: 128, world: { x: 1504, y: 2480 }, connectsTo: 'courtyard-south' },
    west: { edge: 'west', center: 304, from: 256, to: 352, clearWidth: 96, world: { x: 704, y: 2784 }, connectsTo: 'civic-stage-cloister', hostBridge: { x: 608, y: 2736, width: 96, height: 96 } },
    south: { edge: 'south', center: 800, from: 736, to: 864, clearWidth: 128, world: { x: 1504, y: 3056 }, connectsTo: 'preserved-gate-portal-approach' }
  },
  benches: [],
  nativeFeatures: [],
  animation: [],
  layerOrder: ['avenue-base', 'native-avatar', 'avenue-foliage-foreground']
});
export const toWorld = p => ({ x: p.x + AVENUE.worldOrigin.x, y: p.y + AVENUE.worldOrigin.y });
export const fromWorld = p => ({ x: p.x - AVENUE.worldOrigin.x, y: p.y - AVENUE.worldOrigin.y });
export function isPointWalkable(p, { allowBoundary = false } = {}) {
  if (!p || !Number.isFinite(p.x) || !Number.isFinite(p.y)) return false;
  if (!allowBoundary && (p.x < 0 || p.x >= 1472 || p.y < 0 || p.y >= 576)) return false;
  const main = p.x >= 736 && p.x < 864 && (allowBoundary || (p.y >= 0 && p.y < 576));
  const left = p.y >= 256 && p.y < 352 && p.x < 800 && (allowBoundary || p.x >= 0);
  return main || left;
}
export function canStand(p, options = {}) {
  for (let y = 0; y < 16; y += 1) for (let x = -8; x < 8; x += 1) {
    if (!isPointWalkable({ x: p.x + x, y: p.y + y }, options)) return false;
  }
  return true;
}
export function sweep(a, b, options = {}) {
  const n = Math.max(1, Math.ceil(Math.hypot(b.x - a.x, b.y - a.y)));
  for (let i = 0; i <= n; i += 1) {
    if (!canStand({ x: a.x + (b.x - a.x) * i / n, y: a.y + (b.y - a.y) * i / n }, options)) return false;
  }
  return true;
}
