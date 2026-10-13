import fs from 'node:fs'; import path from 'node:path'; import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),sharp=require('sharp');
const R=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const art=fs.readFileSync(R+'/source/lobby-architecture-master.png').toString('base64');
const plaque=(x,y,w,label)=>`<g transform="translate(${x} ${y})"><rect x="1" y="3" width="${w}" height="26" rx="2" fill="#714b26"/><rect width="${w}" height="25" rx="2" fill="#cca567" stroke="#f3d291" stroke-width="2"/><rect x="4" y="4" width="${w-8}" height="17" rx="1" fill="#12383e" stroke="#8d6c3d"/><circle cx="7" cy="12" r="1.5" fill="#f4d598"/><circle cx="${w-7}" cy="12" r="1.5" fill="#f4d598"/><text x="${w/2}" y="16" text-anchor="middle" font-family="DejaVu Sans,sans-serif" font-size="10" font-weight="700" fill="#f7dc9c">${label}</text></g>`;
const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="1152" height="896" viewBox="0 0 1152 896"><image href="data:image/png;base64,${art}" width="1152" height="896"/>${plaque(76,420,120,'UNAVAILABLE')}${plaque(956,420,120,'UNAVAILABLE')}${plaque(516,194,120,'LINK PENDING')}</svg>`;
fs.writeFileSync(R+'/source/lobby-runtime-art.svg',svg);
await sharp(Buffer.from(svg)).png().toFile(R+'/assets/lobby-architecture-native.png');
console.log('Native architecture + physical unavailable/link-pending plaques rendered.');
