const fs=require('fs'),path=require('path'),sharp=require('sharp');const R=path.resolve(__dirname,'..'),m=JSON.parse(fs.readFileSync(R+'/module.json'));
const b64=p=>'data:image/png;base64,'+fs.readFileSync(R+'/'+p).toString('base64');
const img=(p,x,y,w,h)=>`<image href="${b64(p)}" x="${x}" y="${y}" width="${w}" height="${h}"/>`;
const svg=(body,w=640,h=1152)=>`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${body}</svg>`;
const render=async(name,body,w=640,h=1152)=>{fs.writeFileSync(R+'/art-source/'+name+'.svg',svg(body,w,h));await sharp(Buffer.from(svg(body,w,h))).png().toFile(R+'/assets/'+name+'.png');};
(async()=>{
 await render('architecture-native',img('art-source/civic-architecture-master.png',0,0,640,1152));
 const p=img('art-source/podium-master.png',0,0,80,96);await render('podium-native',p,80,96);await render('podium-foreground-native',`<defs><clipPath id="rim"><path d="M8 24H30V31H50V24H72V48H8Z"/></clipPath></defs><g clip-path="url(#rim)">${p}</g>`,80,96);
 let furniture='',foreground='';for(const s of m.students){furniture+=img('assets/student-station-native.png',...s.stationOrigin,96,128);foreground+=`<svg x="${s.stationOrigin[0]}" y="${s.stationOrigin[1]}" width="96" height="128" viewBox="144 112 96 128">${img('assets/station-foreground-source.png',0,0,512,384)}</svg>`;}
 for(const s of m.audience){furniture+=img('assets/chair-north-native.png',...s.chairOrigin,48,64);foreground+=img('assets/chair-north-foreground-native.png',...s.chairOrigin,48,64);}furniture+=img('assets/podium-native.png',...m.speaker.podiumOrigin,80,96);foreground+=img('assets/podium-foreground-native.png',...m.speaker.podiumOrigin,80,96);
 await render('furniture-native',furniture);await render('foreground-native',foreground);
 await render('glass-native','<g fill="#97cebf" fill-opacity=".10"><rect x="65" y="220" width="12" height="112"/><rect x="563" y="220" width="12" height="112"/><rect x="65" y="864" width="12" height="84"/><rect x="563" y="864" width="12" height="84"/></g>');
 await render('shadow-native','<g fill="#242344" fill-opacity=".12"><path d="M66 268V292L128 342H150Z"/><path d="M66 916V940L144 1004H164Z"/></g>');
 let avatars='';for(const a of [...m.students,...m.audience,m.teacher,m.speaker])avatars+=`<svg x="${a.center[0]-16}" y="${a.center[1]-16}" width="32" height="32" viewBox="${a.frame%3*32} ${Math.floor(a.frame/3)*32} 32 32">${img('assets/greg.png',0,0,96,128)}</svg>`;
 const layers=['architecture-native','furniture-native'].map(n=>img('assets/'+n+'.png',0,0,640,1152)).join(''),overlays=['foreground-native','glass-native','shadow-native'].map(n=>img('assets/'+n+'.png',0,0,640,1152)).join('');
 for(const [name,body]of [['civic-empty-native',layers+overlays],['civic-occupied-native',layers+avatars+overlays]]){await sharp(Buffer.from(svg(body))).png().toFile(R+'/docs/'+name+'.png');}
 for(const [name,x,y,w,h]of[['classroom',64,64,512,448],['great-hall',64,576,512,512],['speaker',264,640,112,112],['student',112,176,96,128],['attendee',224,784,64,96]])await sharp(R+'/docs/civic-occupied-native.png').extract({left:x,top:y,width:w,height:h}).png().toFile(R+'/docs/'+name+'-occupied-native.png');
 console.log('Rendered native layers and occupied proof. Greg remains source pixels at 1x.');
})();
