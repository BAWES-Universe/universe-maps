const fs=require('fs'),sharp=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const D=process.env.OUTPUT_DIR||'/tmp/azure-layout-scaffold',W=1280,H=1024,T=32,C=40,R=32;
const rect=(x,y,w,h,fill,extra='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" ${extra}/>`;
const path=(d,stroke,width=1,extra='')=>`<path d="${d}" fill="none" stroke="${stroke}" stroke-width="${width}" ${extra}/>`;
const ellipse=(x,y,rx,ry,fill,extra='')=>`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${fill}" ${extra}/>`;
const svg=body=>`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><defs><linearGradient id="sea" x2="0.8" y2="1"><stop stop-color="#a9e8e3"/><stop offset=".5" stop-color="#58b8c2"/><stop offset="1" stop-color="#247d9b"/></linearGradient><linearGradient id="stone" x2="0" y2="1"><stop stop-color="#fcf4df"/><stop offset="1" stop-color="#dedaca"/></linearGradient><linearGradient id="pool" x2="0" y2="1"><stop stop-color="#126b80"/><stop offset="1" stop-color="#49bbbf"/></linearGradient><linearGradient id="glass" x2=".7" y2="1"><stop stop-color="#c3ebed" stop-opacity=".7"/><stop offset="1" stop-color="#5aa3ab" stop-opacity=".25"/></linearGradient><filter id="shadow" x="-40%" y="-40%" width="180%" height="200%"><feGaussianBlur stdDeviation="4"/></filter></defs>${body}</svg>`;
let a=rect(0,0,W,H,'url(#sea)');
for(let y=24;y<H;y+=38)for(let x=(y%76?0:42);x<W;x+=115)a+=path(`M${x} ${y} q24 -5 48 0 t48 0`,'#d4fbef',1.2,'opacity=".17"');
a+=path('M0 80 Q300 45 600 80 T1280 80','#edfcf4',3,'opacity=".4"');
// Restrained coastal detail at native resolution: shallow seabed and irregular foam.
for(let i=0;i<170;i++){let x=(i*179)%W,y=(i*97)%H;if((x<100||x>1180)||y<110)a+=ellipse(x,y,8+i%13,3+i%5,['#bce3c5','#539b9f','#d9e9bf'][i%3],`opacity="${.035+(i%5)*.012}"`);}
for(let k=0;k<4;k++){let y=814+k*9;a+=path(`M10 ${y} Q90 ${y-16} 115 ${y} T240 ${y+4} T420 ${y+1}`,'#e6fff2',1.2,`opacity="${.2-k*.03}"`);a+=path(`M850 ${y} Q930 ${y-16} 980 ${y} T1160 ${y+4} T1280 ${y+1}`,'#e6fff2',1.2,`opacity="${.2-k*.03}"`);}
// Single continuous stone footprint: every exposed paved pixel is navigable except explicit furniture, walls and basin.
a+=path('M144 400H1136V816H816V976H496V816H144Z','#215b6e',22,'opacity=".22" filter="url(#shadow)"');
a+=rect(128,384,1024,416,'url(#stone)')+rect(480,800,320,160,'url(#stone)');
// fine native-resolution limestone joints, not pixel-upscaled textures
for(let y=384;y<800;y+=32)for(let x=128;x<1152;x+=64)a+=rect(x,y,64,32,'none','stroke="#b8b9aa" stroke-opacity=".30" stroke-width=".7"');
for(let y=800;y<960;y+=32)for(let x=480;x<800;x+=64)a+=rect(x,y,64,32,'none','stroke="#b8b9aa" stroke-opacity=".3" stroke-width=".7"');
// Fine limestone grain and warm hairline veining; not a repeated pixel texture.
for(let i=0;i<7000;i++){let x=128+(i*73.117)%1024,y=384+(i*43.791)%416;a+=ellipse(x,y,.35+(i%3)*.15,.3,['#836f55','#fffaf0'][i%2],'opacity=".10"');}
for(let i=0;i<60;i++){let x=144+(i*137)%970,y=400+(i*53)%370;a+=path(`M${x} ${y}q7 -2 14 1t9 -1`,'#a59e87',.4,'opacity=".15"');}
// Brass inlay stays purely decorative and walkable.
a+=path('M144 400H1136V784H784V944H496V784H144Z','#b69b60',2);
a+=path('M152 408H1128V776H776V936H504V776H152Z','#f9fcf1',2);
// perimeter rail footprint is outside walkway; generous routes have no obstacles at junctions
for(const [x,y,w,h] of [[112,384,16,416],[1152,384,16,416],[128,800,352,16],[800,800,352,16],[464,816,16,144],[800,816,16,144],[480,960,320,16]]){a+=rect(x,y,w,h,'#8aa8a4')+rect(x+2,y+2,w-4,h-4,'#e8f2df');}
for(let x=128;x<=1152;x+=64)if(x<480||x>800)a+=rect(x,795,5,21,'#54777b');
for(let y=400;y<800;y+=64)a+=rect(114, y,12,4,'#52767a')+rect(1154,y,12,4,'#52767a');
// lounge structure, unmistakable walls and a broad open south threshold
const building=rect(320,128,640,256,'#285d67')+rect(352,160,576,224,'#e9e8db');a+=building;
for(let y=160;y<384;y+=32)for(let x=352;x<928;x+=32)a+=rect(x,y,32,32,(x/32+y/32)%2?'#e9e8dc':'#e3e5d9');
a+=rect(320,128,640,32,'#215462')+rect(324,132,632,4,'#e1bf7c')+rect(324,150,632,3,'#ddc28b');
a+=rect(320,160,32,224,'#4c8790')+rect(928,160,32,224,'#4c8790');
for(let y=168;y<368;y+=48)a+=rect(326,y,19,37,'#9dd3cf')+rect(935,y,19,37,'#9dd3cf');
a+=rect(320,352,96,32,'#275966')+rect(864,352,96,32,'#275966');
a+=rect(328,356,80,3,'#dbbb76')+rect(872,356,80,3,'#dbbb76');
a+=rect(416,380,448,4,'#c2ac77');
// Sunlight through the glass and elegant geometric terrazzo at the lounge threshold.
a+=`<path d="M366 192L417 192L570 352L516 352Z M492 192L518 192L670 352L642 352Z M688 192L746 192L899 352L840 352Z" fill="#fff9dc" opacity=".28"/>`;
for(let x=432;x<864;x+=32)a+=path(`M${x} 362l8 -8 8 8 -8 8Z`,'#b4a272',1);
// rear cocktail ledge, art-deco fans, no route behind it
for(const x of [352,800]){a+=rect(x,160,128,32,'#396a70')+rect(x,160,128,7,'#e8c98c');for(let i=0;i<5;i++)a+=path(`M${x+48} 183 L${x+12+i*18} 164`,'#c8b57f',1);}
// typography placed on blocked upper wall, not across the walking floor
// 64px planted beds: raised curbs and dense leaf shapes never resemble paving
function planter(x,y){let s=rect(x+3,y+5,60,60,'#39636a','opacity=".2" filter="url(#shadow)"')+rect(x,y,64,64,'#bcae86','rx="5"')+rect(x+4,y+4,56,56,'#2e6960','rx="3"');for(let i=0;i<11;i++){let px=x+12+(i*17%41),py=y+11+(i*23%42);s+=ellipse(px,py,9,5,['#72a77d','#abc28b','#448773'][i%3],`transform="rotate(${i*31} ${px} ${py})"`);}// Layered palm fronds and ivory agapanthus sit wholly within the raised bed.
for(let k=0;k<9;k++){let ang=k*Math.PI*2/9,dx=Math.cos(ang),dy=Math.sin(ang),cx=x+32,cy=y+30,tx=cx+dx*25,ty=cy+dy*25;s+=`<path d="M${cx} ${cy} Q${cx+dx*12-dy*7} ${cy+dy*12+dx*7} ${tx} ${ty} Q${cx+dx*15+dy*3} ${cy+dy*15-dx*3} ${cx} ${cy}" fill="${['#427e64','#7aa574','#aac18b'][k%3]}"/>`;s+=path(`M${cx} ${cy}L${tx} ${ty}`,'#c0cf96',.65,'opacity=".7"');}
for(let i=0;i<8;i++){let px=x+10+(i*19%44),py=y+10+(i*13%44);s+=ellipse(px,py,2,2,'#f3e8c9')+ellipse(px+2,py+2,1.3,1.3,'#e4d8b6');}
return s;}
for(const p of [[192,448],[1024,448],[192,672],[1024,672]])a+=planter(...p);
// Fountain footprint exactly 4x4 collision tiles; clipped pool and brass concentric details.
a+=rect(579,518,128,128,'#39636a','rx="16" opacity=".2" filter="url(#shadow)"')+rect(576,512,128,128,'#c8b98f','rx="13"')+rect(579,515,122,122,'#fff0cb','rx="11"')+rect(585,521,110,110,'#256d7c','rx="8"')+rect(589,525,102,102,'url(#pool)','rx="7"');
a+=ellipse(640,578,20,12,'#1b687b','opacity=".6"')+ellipse(640,572,13,9,'#f3e5bb')+rect(635,548,10,23,'#d8d5b6','rx="4"')+ellipse(640,549,17,7,'#fcf1cf')+ellipse(640,547,12,4,'#5ac6ce');
// Art Deco basin engravings; edge stays inside its solid footprint.
for(let x=592;x<696;x+=16)a+=path(`M${x} 516l4 3 4 -3 M${x} 636l4 -3 4 3`,'#c0a365',.8);
// compact native-scale furniture: 32px table footprint and 22px cushions.
const seats=[];function table(x,y){a+=ellipse(x+16,y+23,24,13,'#527176','opacity=".18"')+rect(x,y,32,32,'#c1a36a','rx="7"')+rect(x+2,y+1,28,28,'#fff5d9','rx="6"')+ellipse(x+16,y+14,6,4,'#2b7e83')+ellipse(x+16,y+12,4,3,'#82bba6');}
function chair(id,x,feet,side){const y=feet-20; a+=ellipse(x+3,feet-1,15,6,'#486970','opacity=".18"')+rect(x-12,y,24,22,'#bd9d65','rx="5"')+rect(x-10,y+2,20,17,'#3d9295','rx="4"')+rect(x+(side<0?-13:9),y-1,5,23,'#286a72','rx="2"')+path(`M${x-6} ${y+5}V${y+15}`,'#8ac7bf',1);seats.push({id,x,y:feet,side});}
for(const x of [448,800]){table(x,256);chair(x===448?'lounge-west-outer':'lounge-east-inner',x-32,272,-1);chair(x===448?'lounge-west-inner':'lounge-east-outer',x+64,272,1);}
table(624,864);chair('overlook-west',576,880,-1);chair('overlook-east',704,880,1);
// small deco sunburst inlay, intentionally unobstructed on both promenade wings
for(const x of [352,928]){a+=ellipse(x,592,38,38,'none','stroke="#c5b17d" stroke-width="1"');for(let i=0;i<12;i++){let q=i*Math.PI/6;a+=path(`M${x+24*Math.cos(q)} ${592+24*Math.sin(q)}L${x+36*Math.cos(q)} ${592+36*Math.sin(q)}`,'#c5b17d',1);}a+=ellipse(x,592,20,20,'none','stroke="#c5b17d"');}
// Rich fan medallions inset flush with the promenade: fully walkable.
for(const cx of [352,928]){a+=ellipse(cx,592,43,43,'#d3c49b','opacity=".3"')+ellipse(cx,592,40,40,'#275d68','opacity=".88"')+ellipse(cx,592,37,37,'none','stroke="#d4bd80" stroke-width="1.2"');for(let i=0;i<13;i++){let q=Math.PI+i*Math.PI/12,x=cx+Math.cos(q)*34,y=606+Math.sin(q)*43;a+=path(`M${cx} 612 L${x} ${y}`,'#d5c18d',1);}a+=path(`M${cx-28} 613H${cx+28} M${cx-22} 618H${cx+22}`,'#d5c18d',1.5);}
// Strong northern silhouette: stepped parapet, brass fluting and a rising-sun crest, all above blocked wall.
a+=rect(492,113,296,15,'#326b75')+rect(524,98,232,15,'#326b75')+rect(556,87,168,11,'#326b75')+path('M492 116H788M524 101H756M556 90H724','#dfc285',2);
for(let x=508;x<=772;x+=16)a+=path(`M${x} 119V126`,'#abc7ba',1);
a+=`<path d="M604 124A36 31 0 0 1 676 124Z" fill="#d2b87c"/>`;
for(let i=0;i<11;i++){let q=Math.PI+i*Math.PI/10;a+=path(`M640 124L${640+Math.cos(q)*31} ${124+Math.sin(q)*27}`,'#4d7b7c',1);}
let roof=rect(316,116,648,264,'url(#glass)','rx="8"');for(let x=320;x<=960;x+=64)roof+=path(`M${x} 120V376`,'#d6e9d9',3);for(let y=120;y<=376;y+=64)roof+=path(`M320 ${y}H960`,'#e3ecdc',3);roof+=path('M320 120H960V376H864M416 376H320Z','#bc9f65',4);
const props=(name,value,type='bool')=>({name,type,value});
const layer=(name,data,id,extra={})=>({id,name,type:'tilelayer',width:C,height:R,x:0,y:0,visible:true,opacity:1,data,...extra});
const block=Array(C*R).fill(false);const mark=(x,y,w,h)=>{for(let j=y/32;j<(y+h)/32;j++)for(let i=x/32;i<(x+w)/32;i++)block[j*C+i]=true;};
for(let y=0;y<R;y++)for(let x=0;x<C;x++)block[y*C+x]=!((x>=4&&x<36&&y>=12&&y<25)||(x>=15&&x<25&&y>=25&&y<30)||(x>=10&&x<30&&y>=4&&y<12));
for(const b of [[320,128,640,32],[320,160,32,224],[928,160,32,224],[320,352,96,32],[864,352,96,32],[352,160,128,32],[800,160,128,32],[576,512,128,128],[192,448,64,64],[1024,448,64,64],[192,672,64,64],[1024,672,64,64],[448,256,32,32],[800,256,32,32],[624,864,32,32]])mark(...b);
// Unique atlas tiles preserve all smooth native-size vector detail, no enlarged source pixels.
(async()=>{fs.mkdirSync(D,{recursive:true});fs.writeFileSync(D+'/artwork.svg',svg(a));await sharp(Buffer.from(svg(a))).png().toFile(D+'/coastal.png');await sharp(Buffer.from(svg(roof))).png().toFile(D+'/glass.png');await sharp({create:{width:64,height:32,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).png().toFile(D+'/logic.png');
// 16 frame fountain animation; 16 world cells, each tile's frames kept together.
const comps=[],anim=[];for(let cell=0;cell<16;cell++){let col=cell%4,row=Math.floor(cell/4);for(let f=0;f<16;f++){let t=f/16;let b=`<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><defs><clipPath id="p"><rect x="13" y="13" width="102" height="102" rx="7"/></clipPath></defs><g clip-path="url(#p)">`;for(let k=0;k<3;k++){let phase=(t+k/3)%1,r=8+phase*43;b+=ellipse(64,64,r,r*.75,'none',`stroke="#dcffff" stroke-width="1.7" opacity="${.75*(1-phase)}"`);}for(let k=0;k<4;k++){let ang=k*Math.PI/2,dx=Math.cos(ang),dy=Math.sin(ang);b+=path(`M${64+dx*10} ${36+dy*4} Q${64+dx*37} ${19+dy*14} ${64+dx*35} ${67+dy*30}`,'#b4f3f0',2.5,'opacity=".75"');let u=t;let px=(1-u)**2*(64+dx*10)+2*(1-u)*u*(64+dx*37)+u*u*(64+dx*35);let py=(1-u)**2*(36+dy*4)+2*(1-u)*u*(19+dy*14)+u*u*(67+dy*30);b+=ellipse(px,py,2.3,3.4,'#fffce2');}b+='</g></svg>';const tile=await sharp(Buffer.from(b)).extract({left:col*32,top:row*32,width:32,height:32}).png().toBuffer();comps.push({input:tile,left:f*32,top:cell*32});}anim.push({id:cell*16,animation:Array.from({length:16},(_,f)=>({tileid:cell*16+f,duration:70}))});}await sharp({create:{width:512,height:512,channels:4,background:{r:0,g:0,b:0,alpha:0}}}).composite(comps).png().toFile(D+'/fountain.png');
const full=Array.from({length:C*R},(_,i)=>i+1),roofData=full.map((v,i)=>{const x=i%C,y=Math.floor(i/C);return x>=9&&x<=30&&y>=3&&y<12?v+1280:0});const water=Array(C*R).fill(0);for(let c=0;c<16;c++)water[(16+Math.floor(c/4))*C+18+c%4]=2563+c*16;
const ts=(name,image,firstgid,count=1280,cols=40,iw=1280,ih=1024)=>({firstgid,name,image,imagewidth:iw,imageheight:ih,tilewidth:32,tileheight:32,columns:cols,tilecount:count,margin:0,spacing:0});
const start=Array(C*R).fill(0);start[22*C+20]=2561;
const map={type:'map',version:'1.10',tiledversion:'1.11.2',orientation:'orthogonal',renderorder:'right-down',width:C,height:R,tilewidth:32,tileheight:32,infinite:false,nextlayerid:9,nextobjectid:2,properties:[props('name','Azure Pavilion','string'),props('wokaScale',1,'int'),props('script','scene.js','string')],tilesets:[ts('coastal','coastal.png',1),ts('glass','glass.png',1281),{...ts('logic','logic.png',2561,2,2,64,32),tiles:[{id:0,properties:[props('start',true)]},{id:1,properties:[props('collides',true)]}]},{...ts('fountain','fountain.png',2563,256,16,512,512),tiles:anim}],layers:[layer('Coastal architecture',full,1),layer('Solid boundaries and objects',block.map(v=>v?2562:0),2),layer('start',start,3),layer('native-audio',full.map(()=>2561),4),layer('Fountain motion',water,5),{id:6,name:'floorLayer',type:'objectgroup',visible:true,opacity:1,draworder:'topdown',objects:[]},layer('Glass canopy',roofData,7),{id:8,name:'interaction-anchors',type:'objectgroup',visible:true,opacity:1,objects:[{id:1,name:'pavilion-actions',type:'',x:480,y:400,width:320,height:160,rotation:0,visible:true}]}]};
// native-audio cannot reuse the start tile or it broadens spawn! logic tile 0 is transparent only; start is a layer property.
map.tilesets[2].tiles[0].properties=[];map.layers[2].properties=[props('start',true)];
fs.writeFileSync(D+'/azure.tmj',JSON.stringify(map)+'\n');fs.writeFileSync(D+'/geometry.json',JSON.stringify({width:W,height:H,tile:32,seats,tables:[[448,256,32,32],[800,256,32,32],[624,864,32,32]],blocked:block,spawn:{x:656,y:720}},null,2)+'\n');console.log('Built original artwork, map and fountain frames',seats);})();
