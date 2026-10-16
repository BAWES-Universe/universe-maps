// Retain the reviewed circulation graph; register refined artwork to native seats.
const fs=require('fs'),sharp=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');const root='/workspace/azure-expanded';
(async()=>{const g=JSON.parse(fs.readFileSync(root+'/source/polish-before/art-geometry.json')),before=JSON.parse(fs.readFileSync(root+'/source/polish-before/geometry.json')),audit={seats:[],plantIntrusions:[]};
for(const id of ['hub','cafe','lounge','garden','gathering']){const origin=id==='hub'?[2176,2176]:g.areas[id].origin;const{data,info}=await sharp(root+(id==='hub'?'/hub.png':'/source/transparent-islands/'+id+'.png')).ensureAlpha().raw().toBuffer({resolveWithObject:true});function rgb(x,y){const k=(y*info.width+x)*4;return[data[k],data[k+1],data[k+2]];}
for(const s of g.seats.filter(s=>s.island===id)){const old=[s.x,s.y];let sx=s.x-origin[0],sy=s.y-origin[1];if(id==='lounge'&&Number(s.id.split('-')[1])<3)sy+=32;let sumx=0,sumy=0,n=0;for(let y=sy-16;y<=sy+16;y++)for(let x=sx-16;x<=sx+16;x++){const[r,gg,b]=rgb(x,y);if(gg>r*1.35&&b>r*1.3&&gg>35&&gg<170){sumx+=x;sumy+=y;n++;}}if(n<50)throw Error('Cushion not found: '+s.id);s.x=origin[0]+Math.round(sumx/n);s.y=origin[1]+Math.round(sumy/n);audit.seats.push({id:s.id,old,now:[s.x,s.y],pixels:n});}
// Block only newly substantial foliage on previously walkable edge cells.
for(let y=0;y<info.height;y+=32)for(let x=0;x<info.width;x+=32){const wx=origin[0]+x,wy=origin[1]+y,i=wy/32*160+wx/32;if(before.blocked[i])continue;let green=0,center=0;for(let yy=0;yy<32;yy++)for(let xx=0;xx<32;xx++){const[r,gg,b]=rgb(x+xx,y+yy);if(gg>r*1.12&&gg>b*1.15&&gg>45){green++;if(xx>=8&&xx<24&&yy>=8&&yy<24)center++;}}if(green>512&&center>128){g.furniture.push({island:id,kind:'solid',x:wx,y:wy,w:32,h:32});audit.plantIntrusions.push([id,wx,wy]);}}
}
for(const s of g.seats)for(const[x,y]of[[s.x,s.y],[s.x+(s.approachX||0),s.y-s.approachDistance]]){const xx=Math.floor(x/32)*32,yy=Math.floor(y/32)*32;if(!g.floors.some(r=>r[0]===xx&&r[1]===yy))g.floors.push([xx,yy,32,32]);}
// Repaired curved shore ends before the former clipped outermost beach cell.
g.furniture.push({island:'garden',kind:'solid',x:3136,y:4384,w:32,h:32});
g.furniture.push({island:'cafe',kind:'solid',x:2368,y:1152,w:64,h:128},{island:'cafe',kind:'solid',x:2688,y:1152,w:64,h:128});
g.floors.push([1216,2432,32,32]);
const wall=g.furniture.find(f=>f.island==='lounge'&&f.kind==='solid'&&f.x===416&&f.y===2272);wall.h=64;
// Added shelf frontage remains above the moved rear seats and their approach row.
g.notes='Reviewed original circulation graph with registered polished artwork; native seat targets remeasured. New foliage and lounge shelf frontage blocked. Fresh gameplay acceptance required.';
fs.writeFileSync(root+'/source/art-geometry.json',JSON.stringify(g,null,2));fs.writeFileSync(root+'/review/polish-geometry-audit.json',JSON.stringify(audit,null,2));console.log(audit);
})();
