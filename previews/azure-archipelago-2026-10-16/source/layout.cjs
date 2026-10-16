const fs=require('fs'),sharp=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const root='/workspace/azure-expanded';
const islands=[{id:'cafe',x:1952,y:64,entrance:'south'},{id:'garden',x:1952,y:3840,entrance:'north'},{id:'lounge',x:64,y:1952,entrance:'east'},{id:'gathering',x:3840,y:1952,entrance:'west'}];
const bridges=[[2432,1280,256,896],[2432,2944,256,896],[1280,2432,896,256],[2944,2432,896,256]];
const rect=(x,y,w,h,fill,more='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" ${more}/>`;
const svg=(w,h,s)=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}">${s}</svg>`;
const shapes={};let furniture=[];
for(const a of islands){let s=rect(0,0,1216,1216,'#3fadb7')+rect(32,32,1152,1152,'#315b60')+rect(64,64,1088,1088,'#efe2c3');
// Landings preserve eight fully clear grid cells.
if(a.entrance==='south')s+=rect(480,1152,256,64,'#efe2c3');if(a.entrance==='north')s+=rect(480,0,256,64,'#efe2c3');if(a.entrance==='east')s+=rect(1152,480,64,256,'#efe2c3');if(a.entrance==='west')s+=rect(0,480,64,256,'#efe2c3');
for(let v=64;v<1152;v+=32)s+=`<path d="M64 ${v}H1152 M${v} 64V1152" stroke="#ad9d78" stroke-width=".5" opacity=".25"/>`;
const block=(kind,x,y,w,h)=>{furniture.push({island:a.id,kind,x:a.x+x,y:a.y+y,w,h});s+=rect(x,y,w,h,kind==='plants'?'#40846d':kind==='table'?'#c5a96f':'#366b70','rx="8"');};
const seat=(x,y)=>{furniture.push({island:a.id,kind:'seat',x:a.x+x,y:a.y+y,w:32,h:32});s+=rect(x-12,y-20,24,24,'#237a80','rx="4" stroke="#b99c60" stroke-width="3"');};
for(const p of [[96,96],[992,96],[96,992],[992,992]])block('plants',...p,128,128);
if(a.id==='cafe'){block('wall',256,128,704,64);for(const [x,y]of [[352,352],[800,352],[352,736],[800,736]]){block('table',x,y,64,64);seat(x-48,y+48);seat(x+112,y+48);}}
if(a.id==='lounge'){block('wall',256,256,704,32);block('wall',224,256,32,576);block('wall',256,800,704,32);for(const[x,y]of [[384,480],[704,480]]){block('table',x,y,64,64);seat(x-48,y+48);seat(x+112,y+48);}for(const x of[496,624,752])seat(x,336);}
if(a.id==='garden'){for(const p of[[256,256],[768,256],[256,768],[768,768]])block('plants',...p,192,192);block('fountain',544,544,128,128);for(const[x,y]of[[496,336],[720,336],[496,912],[720,912]])seat(x,y);}
if(a.id==='gathering'){for(const[x,y]of[[352,320],[800,320],[352,768],[800,768]]){block('table',x,y,64,64);seat(x-48,y+48);seat(x+112,y+48);}s+=`<circle cx="608" cy="608" r="128" fill="none" stroke="#ba9c58" stroke-width="4"/>`;}
shapes[a.id]=s;
}
let overview=rect(0,0,5120,5120,'#3fadb7');for(const[x,y,w,h]of bridges)overview+=rect(x-32,y-32,w+64,h+64,'#315b60')+rect(x,y,w,h,'#efe2c3');overview+=rect(2176,2176,768,768,'#efe2c3')+rect(2496,2496,128,128,'#257e8a','rx="20"');for(const a of islands)overview+=`<g transform="translate(${a.x} ${a.y})">${shapes[a.id]}</g>`;
(async()=>{for(const a of islands){const data=svg(1216,1216,shapes[a.id]);fs.writeFileSync(`${root}/source/${a.id}-guide.svg`,data);await sharp(Buffer.from(data)).png().toFile(`${root}/source/${a.id}-guide.png`);}fs.writeFileSync(root+'/source/layout.svg',svg(5120,5120,overview));await sharp(Buffer.from(svg(5120,5120,overview))).resize(1280,1280).png().toFile(root+'/review/early-layout.png');fs.writeFileSync(root+'/source/layout.json',JSON.stringify({width:5120,height:5120,tile:32,islands,bridges,hub:[2176,2176,768,768],furniture,clearBridgeTiles:8,status:'draft; not gameplay accepted; not published'},null,2));})();
