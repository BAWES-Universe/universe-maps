import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
const require=createRequire(import.meta.url), sharp=require('sharp');
const R=path.resolve(path.dirname(new URL(import.meta.url).pathname),'..');
const data=p=>'data:image/png;base64,'+fs.readFileSync(path.join(R,p)).toString('base64');
const art=data('source/forum-architecture-master.png'), sheet=data('references/greg-reference.png');
const chair=data('references/chair-below-safe.png'), chairFront=data('references/chair-foreground-safe.png');
const sprite=(x,y,frame)=>`<svg x="${x}" y="${y}" width="32" height="32" viewBox="${frame%3*32} ${Math.floor(frame/3)*32} 32 32" overflow="hidden"><image href="${sheet}" x="0" y="0" width="96" height="128" image-rendering="pixelated"/></svg>`;
const chairImg=(p,front=false)=>`<image x="${p.x-16}" y="${p.y-16}" width="32" height="48" href="${front?chairFront:chair}" image-rendering="pixelated"/>`;
const rows=[
 {row:'A',x:336,ys:[336,368,400,432,464,464,464,464,432,400,368,336]},
 {row:'B',x:272,ys:[336,400,432,464,496,528,528,528,528,528,528,496,464,432,400,336]},
 {row:'C',x:208,ys:[336,400,432,496,528,560,592,592,624,624,624,624,592,592,560,528,496,432,400,336]},
];
const seats=rows.flatMap(r=>r.ys.map((y,i)=>({id:`${r.row}${String(i+1).padStart(2,'0')}`,x:r.x+i*32,y,row:r.row,frame:10,facing:'north',visibleOccupied:(i+Math.floor(y/32))%3!==0})));
const panel=[{id:'panel-left',x:456,y:195,frame:1},{id:'panel-center',x:512,y:200,frame:1},{id:'panel-right',x:568,y:195,frame:1}];
const referenceActors=[{id:'entry',x:496,y:785,frame:10},{id:'perimeter',x:144,y:528,frame:10},{id:'side-approach',x:816,y:240,frame:4}];
const architecture=`<image href="${art}" x="0" y="0" width="1024" height="896"/>`;
const panelActors=panel.map(p=>sprite(p.x-16,p.y-16,p.frame)).join('');
// A clip of the same unchanged architecture restores the foreground of the low table.
// This is source composition, not an implemented depth layer.
const panelFront=`<defs><clipPath id="table-front"><path d="M393 204L411 211L438 217L464 221L488 224L512 225L536 224L560 221L586 217L612 211L632 204L632 280L393 280Z"/></clipPath></defs><g clip-path="url(#table-front)">${architecture}</g>`;
const empty=architecture+seats.map(p=>chairImg(p)).join('')+seats.map(p=>chairImg(p,true)).join('');
const occupied=architecture+panelActors+panelFront+seats.map(p=>chairImg(p)).join('')+seats.filter(p=>p.visibleOccupied).map(p=>sprite(p.x-16,p.y-16,p.frame)).join('')+referenceActors.map(p=>sprite(p.x,p.y,p.frame)).join('')+seats.map(p=>chairImg(p,true)).join('');
const wrap=body=>`<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="896" viewBox="0 0 1024 896">${body}</svg>`;
for(const [name,body] of [['forum-empty-native',empty],['forum-occupied-native',occupied],['forum-architecture-native',architecture]]){
 const svg=wrap(body);fs.writeFileSync(`${R}/source/${name}.svg`,svg);await sharp(Buffer.from(svg)).png().toFile(`${R}/assets/${name}.png`);
}
fs.writeFileSync(`${R}/source/seats.json`,JSON.stringify(seats,null,2)+'\n');
fs.writeFileSync(`${R}/source/scale-reference-positions.json`,JSON.stringify({world:{width:1024,height:896,tileSize:32},audienceSeatCount:48,panelPlaces:3,rows:rows.map(r=>({row:r.row,count:r.ys.length})),panelActors:panel,referenceActors},null,2)+'\n');
const txt=(x,y,s,size=16,color='#bdd0d1',weight=400)=>`<text x="${x}" y="${y}" font-family="DejaVu Sans,sans-serif" font-size="${size}" fill="${color}" font-weight="${weight}">${s}</text>`;
const lines=(x,y,ss,size=16)=>ss.map((s,i)=>txt(x,y+i*(size+8),s,size)).join('');
const block=(y,title,ss)=>txt(1092,y,title,21,'#f4d595',600)+lines(1092,y+33,ss,16);
const review=`<svg xmlns="http://www.w3.org/2000/svg" width="1480" height="1056" viewBox="0 0 1480 1056"><rect width="1480" height="1056" fill="#0c282e"/>${txt(32,43,'FORUM HALL',29,'#f4d695',700)}${txt(32,75,'Parallel talks + panels · An intimate chamber for closer discussion',17)}${txt(1092,42,'LOCAL CONCEPT 01',16,'#70bebc',600)}${txt(1092,73,'32 × 28 tiles · native32',17)}<svg x="24" y="104" width="1024" height="896" viewBox="0 0 1024 896">${occupied}</svg><path d="M1070 112V981" stroke="#315159"/>${block(145,'48 audience chairs',['Three stepped arcs: 12 + 16 + 20.','Shorter rows wrap around the panel.','Count is visual, not event capacity.'])}${block(288,'Three panel places',['A compact curved table replaces','the flagship’s broad speaker stage.','No speaker names or real program.'])}${block(431,'One continuous perimeter',['A teal circulation loop stays outside','the seating; open south arrival and','two clear side-stage approaches.'])}${block(574,'Original 32 px Woka',['Unchanged original Greg frames.','Audience chair pixels stay unrotated.','Map is shown at native 1:1 scale.'])}${block(717,'One distinct second hall',['Chamfered room, low panel focus,','nested fan seating and close sightlines.','Shared sandstone / gold / teal family.'])}<rect x="1092" y="852" width="352" height="124" rx="8" fill="#153940" stroke="#41636a"/>${txt(1110,882,'DESIGN REVIEW LIMIT',15,'#f4d695',600)}${lines(1110,911,['Static composition only. No TMJ / WAM.','Collisions, media and live room untested.','Room name remains provisional.'],14)}${txt(32,1030,'LOCAL ONLY  ·  No live room or broadcast  ·  No public publication  ·  48 audience seats + 3 illustrated panel places',15,'#aac0c4')}</svg>`;
fs.writeFileSync(`${R}/source/forum-overview.svg`,review);await sharp(Buffer.from(review)).png().toFile(`${R}/review/forum-overview.png`);
const native=`<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="864" viewBox="0 0 1280 864"><rect width="1280" height="864" fill="#0c282e"/>${txt(24,39,'Native scale · Woka32 at 1:1',25,'#f4d695',700)}${txt(24,70,'Unchanged source pixels · No sprite enlargement · Static composition',16)}<svg x="0" y="102" width="640" height="320" viewBox="192 128 640 320">${occupied}</svg><svg x="640" y="102" width="640" height="320" viewBox="160 352 640 320">${occupied}</svg><svg x="0" y="452" width="640" height="320" viewBox="192 576 640 320">${occupied}</svg><svg x="640" y="452" width="640" height="320" viewBox="192 352 640 320">${empty}</svg>${txt(24,439,'Panel + close front arc',15,'#f4d695',600)}${txt(664,439,'Stepped fan seats + perimeter',15,'#f4d695',600)}${txt(24,792,'Rear arc + open south arrival',15,'#f4d695',600)}${txt(664,792,'Empty chair layout at identical scale',15,'#f4d695',600)}${txt(24,835,'Concept only. Native world: 1024 × 896 px / 32 × 28 tiles. Runtime depth, reachability and broadcast are not verified.',15)}</svg>`;
fs.writeFileSync(`${R}/source/native-scale-composition.svg`,native);await sharp(Buffer.from(native)).png().toFile(`${R}/review/native-scale-composition.png`);
console.log(JSON.stringify({audience:seats.length,rows:rows.map(r=>r.ys.length),panelPlaces:panel.length,world:[1024,896],unchangedSpriteSize:[32,32]}));
