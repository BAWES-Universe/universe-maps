/* Quiet campus policy. No global score, entry cue, independent player, or conferencing changes. */
import { CAMPUS_AUDIO_GEOMETRY } from './campus-audio-geometry.mjs';

export const AUDIO_POLICY_VERSION = 1;
export const AUDIO_ASSETS = Object.freeze({ fountain: 'audio/fountain.mp3', cascade: 'audio/cascade-soft.mp3' });
export const FUNCTIONAL_SILENT_ZONES = CAMPUS_AUDIO_GEOMETRY.silentZones;
export const FOUNTAIN_SOURCE = Object.freeze({
  id: 'campus-fountain', kind: 'fountain', scene: 'campus', url: AUDIO_ASSETS.fountain,
  // The main basin in the actual 192px asset placed at (2528,1328).
  center: { x: 2624, y: 1456 }, paintedRect: { x: 2528, y: 1328, width: 192, height: 192 },
  innerRadius: 96, outerRadius: 208, bounds: { x: 2416, y: 1248, width: 416, height: 416 },
  edgeFade: 48, maxGain: 0.06,
});

// Actual falling-water pixels in gate-original.png, scaled 1024x1536 -> 960x1440,
// then translated by gate origin (32,1664). No portal ribbon or distant cliff sources.
const FALL_RECTS = [
  { id: 'west-upper', side: 'west', x: 165, y: 2339, width: 39, height: 85 },
  { id: 'east-upper', side: 'east', x: 819, y: 2339, width: 38, height: 85 },
  { id: 'west-middle', side: 'west', x: 182, y: 2508, width: 31, height: 97 },
  { id: 'east-middle', side: 'east', x: 816, y: 2508, width: 29, height: 97 },
  { id: 'west-lower', side: 'west', x: 194, y: 2773, width: 38, height: 142 },
  { id: 'east-lower', side: 'east', x: 798, y: 2773, width: 34, height: 142 },
];
export const WATERFALL_SOURCES = Object.freeze(FALL_RECTS.map(({ id, side, ...rect }) => {
  const left = side === 'west' ? Math.max(32, rect.x - 80) : 608;
  const right = side === 'west' ? 448 : Math.min(992, rect.x + rect.width + 80);
  return Object.freeze({
    id: 'gate-' + id, kind: 'cascade', scene: 'gate', url: AUDIO_ASSETS.cascade, side,
    paintedRect: rect, center: { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 },
    innerRadius: 120, outerRadius: 260, maxGain: 0.05, edgeFade: 48,
    bounds: { x: left, y: rect.y - 64, width: right - left, height: rect.height + 128 },
  });
}));
const clamp = value => Math.max(0, Math.min(1, value));
const smooth = value => { const x = clamp(value); return x * x * (3 - 2 * x); };
const validPosition = p => p && Number.isFinite(p.x) && Number.isFinite(p.y);
const validBounds = b => b && [b.x, b.y, b.width, b.height].every(Number.isFinite) && b.width > 0 && b.height > 0;
export const feetPosition = p => ({ x: p.x, y: p.y + 16 });
const inside = (p, b) => validBounds(b) && p.x >= b.x && p.x <= b.x + b.width && p.y >= b.y && p.y <= b.y + b.height;

export function getLocalizedWaterGain(position, source) {
  if (!validPosition(position) || !source || !validPosition(source.center) || !validBounds(source.bounds) ||
      !Number.isFinite(source.innerRadius) || source.innerRadius < 0 || !Number.isFinite(source.outerRadius) ||
      source.outerRadius <= source.innerRadius || !Number.isFinite(source.edgeFade) || source.edgeFade <= 0 ||
      !Number.isFinite(source.maxGain) || !['fountain', 'cascade'].includes(source.kind)) return 0;
  const p = feetPosition(position), b = source.bounds;
  if (!inside(p, b)) return 0;
  const distance = Math.hypot(p.x - source.center.x, p.y - source.center.y);
  const radial = 1 - smooth((distance - source.innerRadius) / (source.outerRadius - source.innerRadius));
  const edge = Math.min(p.x - b.x, b.x + b.width - p.x, p.y - b.y, b.y + b.height - p.y);
  return Math.min(source.kind === 'fountain' ? 0.06 : 0.05, Math.max(0, source.maxGain)) * radial * smooth(edge / source.edgeFade);
}

export function getCampusSoundscape(position, { geometry = CAMPUS_AUDIO_GEOMETRY, sources = [FOUNTAIN_SOURCE, ...WATERFALL_SOURCES], silentZones = [] } = {}) {
  const empty = { scene: 'silent', room: null, source: null, levels: { fountain: 0, cascade: 0 }, reason: 'outside-map' };
  if (!validPosition(position)) return { ...empty, reason: 'invalid-position' };
  const p = feetPosition(position);
  const scene = inside(p, geometry.campus) ? 'campus' : inside(p, geometry.gate) ? 'gate' : 'silent';
  if (scene === 'silent') return empty;
  // This is AMBIENCE silence only. It never sets Universe's generic silent property.
  const room = [...geometry.silentZones, ...silentZones].find(zone => inside(p, zone));
  if (room) return { ...empty, scene, room: room.id ?? 'functional-area', reason: 'functional-area' };
  const candidates = sources.filter(source => source?.scene === scene && typeof source.url === 'string' && source.url.length > 0)
    .map(source => ({ source, gain: getLocalizedWaterGain(position, source) })).filter(item => item.gain > 0)
    .sort((a, b) => b.gain - a.gain || a.source.id.localeCompare(b.source.id));
  if (!candidates.length) return { ...empty, scene, reason: 'quiet-default' };
  const { source, gain } = candidates[0];
  // A single strongest eligible native source: nearby falls cannot add their gains.
  return { scene, room: null, reason: 'localized-water', source: { id: source.id, kind: source.kind, url: source.url, volume: gain, loop: true },
    levels: { fountain: source.kind === 'fountain' ? gain : 0, cascade: source.kind === 'cascade' ? gain : 0 } };
}

export class CampusAudioDirector {
  constructor(adapter, policy = {}) { this.adapter = adapter; this.policy = policy; this.disposed = false; this.last = null; this.sent = null; }
  observe(position) {
    if (this.disposed) return;
    this.last = getCampusSoundscape(position, this.policy);
    const source = this.last.source;
    if (!source) { if (this.sent) this.adapter.silence(); this.sent = null; return this.last; }
    if (this.sent?.url !== source.url) this.adapter.setSource(source.url, { volume: source.volume, loop: true });
    else if (Math.abs(source.volume - this.sent.volume) >= 0.0005) this.adapter.setVolume(source.volume);
    else return this.last;
    this.sent = { ...source };
    return this.last;
  }
  dispose() { if (this.disposed) return; this.disposed = true; this.adapter.stop(); this.sent = null; }
}
