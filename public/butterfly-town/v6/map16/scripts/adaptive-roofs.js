/* Per-player roof presentation using the fork's existing native map APIs. */
(() => {
  'use strict';
  const subscriptions = [], visibility = new Map();
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const prop = (object, name) => object.properties?.find(p => p.name === name)?.value;
  const flatten = layers => layers.flatMap(l => l.type === 'group' ? flatten(l.layers) : [l]);
  let disposed = false, positionRevision = 0, configuration, buildings = [], motionLayers = [];
  const fail = message => { throw new Error('Adaptive roof contract: ' + message); };

  // Native area queries use the player's foot point, 16 pixels below the position origin.
  function contains(position, area) {
    const x = position.x, y = position.y + configuration.feetOffsetY;
    return x >= area.x && x < area.x + area.width && y >= area.y && y < area.y + area.height;
  }
  function show(name, value) {
    if (disposed || visibility.get(name) === value) return;
    (value ? WA.room.showLayer : WA.room.hideLayer)(name);
    visibility.set(name, value);
  }
  function reconcile(position) {
    if (disposed || !configuration || !Number.isFinite(position.x) || !Number.isFinite(position.y)) return;
    const inside = buildings.filter(b => b.interiors.some(a => contains(position, a)));
    // Hide only visual artwork. Structural shell, glass, posts and collision never appear here.
    show(configuration.sharedTranslucentLayer, inside.length === 0);
    for (const building of buildings) {
      const isInside = inside.includes(building);
      const approaching = building.approaches.some(a => contains(position, a));
      // An interior takes priority over any overlapping approach event from another building.
      show(building.opaqueLayer, inside.length ? !isInside : !approaching);
    }
  }
  async function refresh() {
    const revision = ++positionRevision;
    try {
      const position = await WA.player.getPosition();
      if (!disposed && revision === positionRevision) reconcile(position);
    } catch (error) {
      if (!disposed) console.warn('Roof position refresh failed.', error);
    }
  }
  function motionChanged() {
    if (disposed) return;
    for (const name of motionLayers) show(name, !media.matches);
  }
  function dispose() {
    if (disposed) return;
    disposed = true;
    ++positionRevision;
    subscriptions.splice(0).forEach(s => s?.unsubscribe?.());
    media.removeEventListener?.('change', motionChanged);
  }

  WA.onInit().then(async () => {
    const map = await WA.room.getTiledMap();
    if (disposed) return;
    const raw = prop(map, 'campusRoofContract');
    if (typeof raw !== 'string') fail('campusRoofContract must contain the compiler-issued JSON string.');
    configuration = JSON.parse(raw);
    if (configuration.version !== 1 || configuration.feetOffsetY !== 16) fail('unsupported version or foot origin.');
    const layers = flatten(map.layers), objects = layers.flatMap(l => l.objects ?? []);
    const findArea = name => {
      const area = objects.find(o => o.name === name && o.class === 'area');
      if (!area || area.rotation || area.polygon || area.ellipse || !(area.width > 0 && area.height > 0)) fail('missing rectangular class=area object: ' + name);
      return area;
    };
    const tilesets = [...map.tilesets].sort((a, b) => b.firstgid - a.firstgid);
    const metadataBySet = new Map(tilesets.map(set => [set, new Map((set.tiles ?? []).map(tile => [tile.id, tile]))]));
    const verifyVisualLayer = name => {
      const layer = layers.find(l => l.type === 'tilelayer' && l.name === name);
      if (!layer || layer.x || layer.y || layer.width !== map.width || layer.height !== map.height) fail('visual layer must have full native map dimensions at zero origin: ' + name);
      if (prop(layer, 'collides') || prop(layer, 'exitUrl') || name === 'start') fail('interactive layer is not a visual roof: ' + name);
      const used = new Set(layer.data.filter(Boolean).map(gid => (gid >>> 0) & 0x1fffffff));
      for (const gid of used) {
        const set = tilesets.find(t => gid >= t.firstgid);
        if (!set) fail('unknown roof tile');
        const tile = metadataBySet.get(set).get(gid - set.firstgid);
        if (tile && ['collides', 'exitUrl', 'exitSceneUrl', 'start', 'startLayer'].some(key => prop(tile, key))) fail('interactive tile in visual layer: ' + name);
      }
      return layer;
    };
    const layerNames = [configuration.sharedTranslucentLayer, ...configuration.buildings.map(b => b.opaqueLayer)];
    if (new Set(layerNames).size !== layerNames.length) fail('roof layer names must be unique.');
    layerNames.forEach(verifyVisualLayer);
    buildings = configuration.buildings.map(b => ({...b, interiors: b.interiorAreas.map(findArea), approaches: b.approachAreas.map(findArea)}));
    motionLayers = configuration.motionLayers ?? [];
    motionLayers.forEach(verifyVisualLayer);
    subscriptions.push(WA.player.onPlayerMove(position => { ++positionRevision; reconcile(position); }));
    const areaNames = new Set(configuration.buildings.flatMap(b => [...b.interiorAreas, ...b.approachAreas]));
    for (const name of areaNames) {
      subscriptions.push(WA.room.area.onEnter(name).subscribe(refresh));
      subscriptions.push(WA.room.area.onLeave(name).subscribe(refresh));
    }
    media.addEventListener?.('change', motionChanged);
    motionChanged();
    await refresh();
  }).catch(error => { if (!disposed) console.error('Adaptive roof initialization failed.', error); });
  window.addEventListener('pagehide', dispose, {once: true});
})();
