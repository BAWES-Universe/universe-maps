import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const sharp = require('sharp');
const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const data = p => 'data:image/png;base64,' + fs.readFileSync(path.join(root, p)).toString('base64');
const architecture = data('source/lobby-architecture-master.png');
const sheet = data('references/greg-reference.png');
const positions = [
  {name:'arrival scale reference', x:560, y:768, frame:10},
  {name:'directory visitor scale reference', x:464, y:672, frame:10},
  {name:'crossroads scale reference', x:688, y:432, frame:4},
  {name:'alcove scale reference', x:272, y:304, frame:10},
];
const sprite = (x,y,frame) => `<svg x="${x}" y="${y}" width="32" height="32" viewBox="${frame%3*32} ${Math.floor(frame/3)*32} 32 32" overflow="hidden"><image href="${sheet}" x="0" y="0" width="96" height="128" image-rendering="pixelated"/></svg>`;
const map = `<image href="${architecture}" width="1152" height="896"/>${positions.map(p=>sprite(p.x,p.y,p.frame)).join('')}`;
const native = `<svg xmlns="http://www.w3.org/2000/svg" width="1152" height="896" viewBox="0 0 1152 896">${map}</svg>`;
fs.writeFileSync(path.join(root,'source/lobby-concept-native.svg'), native);
await sharp(Buffer.from(native)).png().toFile(path.join(root,'assets/lobby-concept-native.png'));

const txt=(x,y,s,size=16,color='#bdcdd0',weight='400')=>`<text x="${x}" y="${y}" font-family="DejaVu Sans,sans-serif" font-size="${size}" fill="${color}" font-weight="${weight}">${s}</text>`;
const lines=(x,y,ss,size=16,color='#bdcdd0',weight='400')=>ss.map((s,i)=>txt(x,y+i*(size+8),s,size,color,weight)).join('');
const block=(y,num,title,ss)=>`<circle cx="1224" cy="${y-5}" r="15" fill="#183d42" stroke="#d4ab65"/>${txt(1219,y,num,14,'#f3d694','600')}${txt(1252,y,title,19,'#f5d495','600')}${lines(1252,y+32,ss,15)}`;
const review=`<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1056" viewBox="0 0 1600 1056">
<rect width="1600" height="1056" fill="#0c282e"/>
${txt(32,43,'ASTRAL CONCOURSE',29,'#f4d695','700')}
${txt(32,75,'A shared arrival for parallel talks, panels and esports',17)}
${txt(1210,42,'CONCEPT 01',16,'#70bebc','600')}
${txt(1210,73,'36 × 28 tiles · 32 px world grid',17)}
<svg x="24" y="104" width="1152" height="896" viewBox="0 0 1152 896">${map}</svg>
<path d="M1194 112V981" stroke="#315159"/>
${block(142,'1','Quiet arrival',['South entry stays clear.','Silent spawn is design intent;','audio is not configured.'])}
${block(278,'2','Orient at reception',['Directory and program boards','are visible from the approach.','All content is sample only.'])}
${block(414,'3','Choose a hall',['Flagship north · Forum west','Arena east. All three portals','are unconfigured concepts.'])}
${block(550,'4','An open crossroads',['No stage, queue barrier or','central furniture. Circulation','continues in every direction.'])}
${block(686,'5','Optional conversation',['Two planted social alcoves','are tucked away from entry','and the main through-routes.'])}
<rect x="1210" y="829" width="350" height="151" rx="8" fill="#153940" stroke="#41636a"/>
${txt(1228,858,'NATIVE SCALE CHECK',15,'#f4d695','600')}
${sprite(1228,880,1)}
<rect x="1228" y="880" width="32" height="32" fill="none" stroke="#76bfbc"/>
${txt(1275,899,'Original 32 × 32 Woka frame',14)}
${lines(1228,936,['Map shown at 1 image px = 1 world px.','Avatars are illustrative scale references.'],13)}
${txt(32,1030,'DESIGN REVIEW ONLY  ·  No TMJ / WAM  ·  No live rooms  ·  No real program or event-capacity claim',15,'#aac0c4')}
</svg>`;
fs.writeFileSync(path.join(root,'source/lobby-concept-review.svg'),review);
await sharp(Buffer.from(review)).png().toFile(path.join(root,'review/lobby-concept-review.png'));
fs.writeFileSync(path.join(root,'source/scale-reference-positions.json'),JSON.stringify({tile_size:32,width_tiles:36,height_tiles:28,map_width:1152,map_height:896,sprites:positions},null,2)+'\n');
console.log('Rendered one concept at native32 scale: 1152×896 map, 1600×1056 review sheet.');
