'use strict';
window.civic={};
civic.canvas=(w=640,h=1152)=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c;};
civic.load=src=>new Promise((res,rej)=>{let i=new Image;i.onload=()=>res(i);i.onerror=rej;i.src=src;});
civic.polygon=(ctx,pts)=>{ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(...p):ctx.moveTo(...p));ctx.closePath();};
civic.init=async()=>{
 const [m,architecture,station,back,chair,chairFg,podium,greg]=await Promise.all([fetch('../module.json').then(r=>r.json()),civic.load('../art-source/civic-architecture-master.png'),civic.load('../assets/student-station-native.png'),civic.load('../assets/station-foreground-source.png'),civic.load('../assets/chair-north-native.png'),civic.load('../assets/chair-north-foreground-native.png'),civic.load('../art-source/podium-master.png'),civic.load('../assets/greg.png')]);
 Object.assign(civic,{m,greg});const canvases={architecture:civic.canvas(),furniture:civic.canvas(),foreground:civic.canvas(),glass:civic.canvas(),shadow:civic.canvas()};let b=canvases.architecture.getContext('2d');b.imageSmoothingEnabled=true;b.imageSmoothingQuality='high';b.drawImage(architecture,0,0,640,1152);
 const f=canvases.furniture.getContext('2d'),fg=canvases.foreground.getContext('2d');f.imageSmoothingEnabled=false;fg.imageSmoothingEnabled=false;
 for(const s of m.students){f.drawImage(station,...s.stationOrigin);const [x,y]=s.stationOrigin;fg.drawImage(back,144,112,96,128,x,y,96,128);}
 for(const s of m.audience){f.drawImage(chair,...s.chairOrigin);fg.drawImage(chairFg,...s.chairOrigin);}
 const nativePodium=civic.canvas(80,96),p=nativePodium.getContext('2d');p.imageSmoothingEnabled=true;p.imageSmoothingQuality='high';p.drawImage(podium,0,0,80,96);f.drawImage(nativePodium,...m.speaker.podiumOrigin);
 const rim=civic.canvas(80,96),r=rim.getContext('2d');r.save();civic.polygon(r,[[8,24],[30,24],[30,31],[50,31],[50,24],[72,24],[72,48],[8,48]]);r.clip();r.drawImage(nativePodium,0,0);r.restore();fg.drawImage(rim,...m.speaker.podiumOrigin);
 // Original code-native above-player shallow window tint. Alpha is intentional,
 // physical perimeter colliders are stored separately and never hidden.
 const g=canvases.glass.getContext('2d');g.fillStyle='rgba(151,206,191,.10)';for(const [x,y,w,h]of[[65,220,12,112],[563,220,12,112],[65,864,12,84],[563,864,12,84]]){g.fillRect(x,y,w,h);}
 const sh=canvases.shadow.getContext('2d');sh.fillStyle='rgba(36,35,68,.12)';for(const points of [[[66,268],[66,292],[128,342],[150,342]],[[66,916],[66,940],[144,1004],[164,1004]]]){civic.polygon(sh,points);sh.fill();}
 Object.assign(civic,{layers:canvases,nativePodium,podiumRim:rim});return civic;
};
civic.drawAvatar=(ctx,a)=>{const col=a.frame%3,row=Math.floor(a.frame/3);ctx.imageSmoothingEnabled=false;ctx.drawImage(civic.greg,col*32,row*32,32,32,a.center[0]-16,a.center[1]-16,32,32);};
civic.compose=(occupied=true)=>{const c=civic.canvas(),ctx=c.getContext('2d');ctx.drawImage(civic.layers.architecture,0,0);ctx.drawImage(civic.layers.furniture,0,0);if(occupied){for(const a of [...civic.m.students,...civic.m.audience,civic.m.teacher,civic.m.speaker])civic.drawAvatar(ctx,a);}ctx.drawImage(civic.layers.foreground,0,0);ctx.drawImage(civic.layers.glass,0,0);ctx.drawImage(civic.layers.shadow,0,0);return c;};
civic.save=async(name,kind,value)=>{let r=await fetch('/qa/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,[kind]:value})});if(!r.ok)throw Error('save '+name+' '+r.status);return r.json();};
civic.export=async()=>{for(const [name,c]of Object.entries(civic.layers))await civic.save('layer-'+name,'png',c.toDataURL());await civic.save('podium-native','png',civic.nativePodium.toDataURL());await civic.save('podium-foreground-native','png',civic.podiumRim.toDataURL());const occupied=civic.compose(true),empty=civic.compose(false);await civic.save('civic-occupied-native','png',occupied.toDataURL());await civic.save('civic-empty-native','png',empty.toDataURL());for(const [name,x,y,w,h]of[['classroom',64,64,512,448],['great-hall',64,576,512,512],['speaker',280,632,112,112],['student',112,176,96,128],['attendee',240,784,64,96]]){let out=civic.canvas(w,h),ctx=out.getContext('2d');ctx.drawImage(occupied,x,y,w,h,0,0,w,h);await civic.save(name+'-occupied-native','png',out.toDataURL());}return true;};
