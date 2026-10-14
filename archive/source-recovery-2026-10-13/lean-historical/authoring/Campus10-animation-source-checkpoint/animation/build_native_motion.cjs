/* Editable vector-authored overlays. PNGs are rendered from these SVG sources,
   not repainted or shifted copies of the campus artwork. */
const fs=require('fs'),path=require('path'),sharp=require('sharp');
const R='/workspace/shared/magical-campus-standard32-09', O=__dirname;
const svg=(w,h,body,defs='')=>`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><defs>${defs}</defs>${body}</svg>`;
const p=(d,c,a=1,w=1)=>`<path d="${d}" fill="none" stroke="${c}" stroke-opacity="${a.toFixed(3)}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
const el=(x,y,rx,ry,c,a=1)=>`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${c}" fill-opacity="${a.toFixed(3)}"/>`;
const paths=[],effects=[];
async function emit(name,origin,size,n,duration,make,options={}){
 const files=[];for(let i=0;i<n;i++){
  const body=make(i,n), src=svg(...size,body.body??body,body.defs??'');
  const stem=`${name}-${String(i).padStart(2,'0')}`;fs.writeFileSync(`${O}/source/${stem}.svg`,src);
  const png=await sharp(Buffer.from(src)).png().toBuffer();
  if(options.mask){await sharp(png).composite([{input:options.mask,blend:'dest-in'}]).png().toFile(`${O}/effects/${stem}.png`);}else fs.writeFileSync(`${O}/effects/${stem}.png`,png);
  files.push(`effects/${stem}.png`);
 }
 effects.push({name,origin,size,frames:files,duration,layer:options.layer??'below',construction:'Editable SVG curves and shapes rasterized at native 1:1; fixed ownership mask; no whole-image translation',...options.meta});
}
const bez=(a,b,c,t)=>[(1-t)*(1-t)*a[0]+2*(1-t)*t*b[0]+t*t*c[0],(1-t)*(1-t)*a[1]+2*(1-t)*t*b[1]+t*t*c[1]];
(async()=>{
 const jets=[[[101,15],[72,-18],[58,80]],[[139,15],[168,-18],[185,86]],[[95,46],[77,39],[68,108]],[[144,45],[162,43],[168,108]],[[84,59],[69,62],[61,99]],[[155,58],[174,68],[178,104]]];
 const basin=`<clipPath id="basin"><path fill-rule="evenodd" d="M15,76 A105,68 0 1 0 225,76 A105,68 0 1 0 15,76 Z M84,20 L153,20 L153,81 L146,94 L128,104 L110,104 L91,94 L84,83 Z"/></clipPath>`;
 await emit('fountain-water',[816,1344],[240,152],16,100,(i,n)=>{
  let b='';
  for(let j=0;j<jets.length;j++){
   const [a,c,z]=jets[j];
   // Persistent thin aqua glaze reduces the baked jet's white peak so highlights can travel.
   b+=p(`M${a} Q${c} ${z}`,'#2faeaa',.40,1.65);
   for(let k=0;k<3;k++){
    const t=(i/n+j*.137+k/3)%1,tail=Math.max(0,t-.06),v=bez(a,c,z,t),u=bez(a,c,z,tail);
    b+=p(`M${u} L${v}`,'#7ffff4',.22,3.8)+p(`M${u} L${v}`,'#f1fff0',.90,1.45)+el(v[0],v[1],1.05,1.5,'#ffffff',.85);
   }
  }
  b+='<g clip-path="url(#basin)">';
  const centers=[[60,108,.03],[178,109,.37],[115,126,.65],[46,81,.21],[193,85,.79]];
  for(const [x,y,offset] of centers){for(let k=0;k<2;k++){
   const t=(i/n+offset+k*.5)%1,rx=2+16*t,ry=1+5*t,alpha=.8*(1-t);
   b+=p(`M${x-rx},${y} a${rx},${ry} 0 0 0 ${rx*2},0`,'#b7fff3',alpha,1.15);
   b+=p(`M${x-rx*.68},${y+2} a${rx*.68},${ry*.65} 0 0 0 ${rx*1.36},0`,'#4bccca',alpha*.55,.9);
  }}
  return {body:b+'</g>',defs:basin};
 },{meta:{purpose:'Descending jet highlights, six distinct water trajectories and staggered expanding basin arcs; stone and pedestal excluded',loopMs:1600}});
 // Main-river ownership: explicit left-bank polygon plus blue-water/alpha test.
 const origin=[2736,1248],size=[208,1024];
 const raw=await sharp(`${R}/layers/campus-base.png`).extract({left:origin[0],top:origin[1],width:size[0],height:size[1]}).ensureAlpha().raw().toBuffer();
 const above=await sharp(`${R}/layers/campus-above.png`).extract({left:origin[0],top:origin[1],width:size[0],height:size[1]}).ensureAlpha().raw().toBuffer();
 const bank=[[0,15],[75,28],[145,39],[240,46],[345,64],[430,69],[525,77],[610,85],[705,90],[775,76],[865,64],[950,72],[1024,86]];
 const edge=y=>{let k=0;while(k+1<bank.length&&bank[k+1][0]<y)k++;const [a,x]=bank[k],[b,z]=bank[Math.min(k+1,bank.length-1)];return x+(z-x)*(y-a)/(b-a||1);};
 const mask=Buffer.alloc(size[0]*size[1]*4);for(let y=0;y<size[1];y++)for(let x=0;x<size[0];x++){
  let q=(y*size[0]+x)*4;const [r,g,b,a]=raw.subarray(q,q+4);let inside=x>=edge(y)&&a>=250&&b>r*1.28&&g>r*1.09&&above[q+3]<8;
  if(inside){mask[q]=mask[q+1]=mask[q+2]=mask[q+3]=255;}
 }
 const riverMask=await sharp(mask,{raw:{width:208,height:1024,channels:4}}).png().toBuffer();fs.writeFileSync(`${O}/source/river-water-owner-mask.png`,riverMask);
 fs.writeFileSync(`${O}/source/river-water-owner-mask.svg`,svg(...size,`<path d="M${bank.map(([y,x])=>`${x},${y}`).join(' L')} L208,1024 L208,0 Z" fill="white"/>`));
 await emit('river-water',origin,size,16,140,(i,n)=>{
  let b='';
  for(let j=0;j<58;j++){
   let row=10+j*17.4,offset=(j*.381966)%1,t=(i/n+offset)%1,alpha=Math.sin(Math.PI*t)**1.3;
   let x=edge(row)+11+((j*37)%Math.max(22,Math.floor(174-edge(row))));
   let y=row+t*27,drift=4*Math.sin((row/137)+t*1.5),len=13+(j%5)*3;
   const d=`M${x+drift},${y} q${len*.36},${-3-j%3} ${len*.6},1 t${len*.4},3`;
   b+=p(d,'#43d9ed',alpha*.12,3.4)+p(d,'#a5f0f3',alpha*.46,1.2);
   if(j%3===0)b+=p(`M${x+drift-5},${y+6} q7,-3 14,1`,'#70d9e8',alpha*.34,.9);
   // Short bright beads travel with the same downstream direction, not independent noise.
   if(j%4===1)b+=el(x+drift+len*.44,y+.7,.95,.75,'#d9ffff',alpha*.58);
  }
  return b;
 },{mask:riverMask,meta:{purpose:'58 staggered downstream ripple groups through the full water corridor including preserved eastern edge; blue-water mask excludes bank stone, plants, rocks and above-layer material',loopMs:2240}});
 const firedefs=`<clipPath id="fire"><path fill-rule="evenodd" d="M10,5 L60,5 L65,57 L38,73 L11,61 Z M6,66 L29,35 L36,29 L41,37 L18,71 Z M34,29 L43,35 L65,61 L57,69 L32,42 Z M25,73 L31,49 L39,40 L44,45 L35,75 Z"/></clipPath>`;
 await emit('fire-flame',[2360,1720],[72,80],12,90,(i,n)=>{
  const q=i/n*Math.PI*2,lean=Math.sin(q)*3.2,top=11+Math.sin(q*2+.7)*2.4,side=22+Math.sin(q+1.4)*3;
  let b=el(36,38,29,28,'#ffae2a',.025+.018*(1+Math.sin(q+.9)));
  // Only the rear tips change shape; painted logs and most painted flame texture stay visible.
  b+='<g clip-path="url(#fire)">';
  b+=`<path d="M29,33 C27,26 ${38+lean},22 ${34+lean},${top} C${43+lean},22 46,28 41,34 Z" fill="url(#flamewarm)" fill-opacity=".76"/>`;
  b+=`<path d="M33,32 C31,27 ${39+lean*.5},24 ${37+lean*.7},${top+6} C43,27 40,30 39,32 Z" fill="url(#flamecore)" fill-opacity=".8"/>`;
  b+=`<path d="M19,37 C17,32 24,29 ${22+Math.sin(q+1)*2},${side+3} C29,30 30,35 27,38 Z" fill="url(#flamewarm)" fill-opacity=".66"/>`;
  b+=`<path d="M44,37 C42,31 48,29 ${51+Math.sin(q+2)*2},${24+Math.sin(q*2)*2} C49,33 55,33 51,39 Z" fill="url(#flamewarm)" fill-opacity=".58"/>`;
  for(let j=0;j<3;j++){let t=(i/n+j*.34)%1,xx=31+j*5+Math.sin(t*4+j)*2.5,yy=25-23*t;b+=el(xx,yy,.65,1.1,'#ffe995',Math.sin(t*Math.PI)*.9);}
  return {body:b+'</g>',defs:firedefs+'<linearGradient id="flamewarm" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0" stop-color="#ff7915" stop-opacity=".08"/><stop offset=".48" stop-color="#ffc922" stop-opacity=".8"/><stop offset="1" stop-color="#ffe583" stop-opacity=".95"/></linearGradient><linearGradient id="flamecore" x1="0%" y1="100%" x2="0%" y2="0%"><stop offset="0" stop-color="#fff2a0" stop-opacity="0"/><stop offset=".5" stop-color="#fffbd1"/><stop offset="1" stop-color="#ffffe8"/></linearGradient>'};
 },{meta:{purpose:'Changing curved flame silhouette and rising embers behind explicit fixed log exclusion polygons, restrained local amber light',loopMs:1080}});
 // One compact life area, above existing foliage. Stems and soil are untouched.
 const lifeOrigin=[1968,1400],lifeSize=[192,96];
 await emit('garden-life',lifeOrigin,lifeSize,16,160,(i,n)=>{
  const q=i/n*Math.PI*2;let b='';
  b+=el(175,38,22,26,'url(#lampglow)',.10+.035*Math.sin(q+.8));
  for(let j=0;j<2;j++){const ph=q+j*2.2,x=46+j*76+Math.sin(ph)*13,y=48+j*8+Math.sin(ph*2)*5,wing=.6+1.7*(.5+.5*Math.sin(q*4+j));b+=el(x-1.2,y,wing,1.5,j?'#99f3ff':'#ffe6a8',.91)+el(x+1.2,y,wing,1.5,j?'#67d8ef':'#ffc67d',.91)+p(`M${x},${y-1.4} v3`,'#715848',.9,.65);}
  return {body:b,defs:'<radialGradient id="lampglow"><stop offset="0" stop-color="#ffdb85" stop-opacity=".85"/><stop offset=".5" stop-color="#ffc061" stop-opacity=".25"/><stop offset="1" stop-color="#ffb84d" stop-opacity="0"/></radialGradient>'};
 },{layer:'above',meta:{purpose:'Two tiny looping insects inside the existing flower bed and one restrained local lantern aura; fixed painted foliage and lamp core retained',loopMs:2560}});
 fs.writeFileSync(`${O}/effects/effects.json`,JSON.stringify({revision:'Campus10-native-vector-motion',effects,notes:['Remove old three-effect specification when integrating these replacements.','Place below effects after base and before floorLayer; place garden-life after campus-above using ordinary Tiled animation cells.','Source baseline is immutable Campus09; final masks must be checked against integrated Campus10 composition.']},null,2)+'\n');
 console.log(JSON.stringify(effects.map(({name,origin,size,frames,duration,layer})=>({name,origin,size,frames:frames.length,duration,layer})),null,2));
})().catch(e=>{console.error(e);process.exit(1)});
