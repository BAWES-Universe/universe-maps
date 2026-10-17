import { defineConfig } from 'vite';
import { readFileSync, writeFileSync, copyFileSync } from 'node:fs';
import { getMaps, getMapsScripts, getMapsOptimizers } from 'wa-map-optimizer-vite';

// Run from this candidate directory. Preserve its native16 collision grid;
// do not change the shared repository configuration or its other maps.
const maps = getMaps('.');
export default defineConfig({
  base: './',
  build: {
    outDir: 'dist',
    rollupOptions: { input: getMapsScripts(maps) },
  },
  plugins: [
    ...getMapsOptimizers(maps, { tile: { size: 16 } }),
    {
      name: 'sky-campus-native-runtime',
      closeBundle: {
        order: 'post',
        sequential: true,
        handler() {
          // The generic optimizer HTML loads a different product's remote iframe API.
          // This self-contained map script must use the current Universe client's API,
          // as it does in the tested source map. A JS property lets the client inject it.
          const file = 'dist/campus.tmj';
          const map = JSON.parse(readFileSync(file, 'utf8'));
          map.properties.find((property: { name: string }) => property.name === 'script').value = 'runtime.js';
          copyFileSync('runtime.js', 'dist/runtime.js');
          writeFileSync(file, JSON.stringify(map));
        },
      },
    },
  ],
});
