#!/usr/bin/env node
// Offline validation against retained WorkAdventure source. No server or media claim.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { stripTypeScriptTypes } from 'node:module';
import { WAMFileFormat } from '../validation/current-source-audit/current-schema.mjs';
import { wamFileMigration } from '../validation/current-source-audit/current-migration.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=path.join(root,'validation/current-source-audit');
const wamPath=path.resolve(process.argv[2]??path.join(root,'map32/astral-concourse-lobby.wam'));
const reportPath=path.resolve(process.argv[3]??path.join(root,'validation/schema-silence.json'));
if(!reportPath.startsWith(root+path.sep))throw new Error('Report must stay within this lobby package');
const checks=[],warnings=[];
const check=(name,pass,details={})=>checks.push({check:name,pass:Boolean(pass),...details});
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
const readJson=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const provenance=readJson(path.join(source,'source-provenance.json'));
for(const f of provenance.files)check('retained source integrity: '+f.file,sha(fs.readFileSync(path.join(source,f.file)))===f.sha256);
const raw=fs.readFileSync(wamPath,'utf8'),wam=JSON.parse(raw);
const parsed=WAMFileFormat.safeParse(wam);
check('pinned current WAM schema',parsed.success,parsed.success?{}:{errors:parsed.error.issues});
try{wamFileMigration.migrate(structuredClone(wam));check('pinned current WAM migration',true);}catch(e){check('pinned current WAM migration',false,{error:e.message});}
check('version matches current migration target',wam.version===wamFileMigration.getLatestVersion());
check('mapUrl is local relative TMJ',typeof wam.mapUrl==='string'&&!/^[a-z]+:|^\/\//i.test(wam.mapUrl)&&wam.mapUrl.endsWith('.tmj'));
const tmjPath=path.resolve(path.dirname(wamPath),wam.mapUrl),tmjRaw=fs.readFileSync(tmjPath,'utf8'),tmj=JSON.parse(tmjRaw);
check('local mapUrl remains inside lobby package',tmjPath.startsWith(root+path.sep));
check('finite orthogonal native32 map',!tmj.infinite&&tmj.orientation==='orthogonal'&&tmj.tilewidth===32&&tmj.tileheight===32);
const properties=o=>Object.fromEntries((o.properties??[]).map(p=>[p.name,p.value]));
const flattened=[];
function flatten(layers){for(const l of layers??[]){flattened.push(l);flatten(l.layers);}}
flatten(tmj.layers);
check('no transformed layers in scoped geometry audit',flattened.every(l=>![l.x,l.y,l.offsetx,l.offsety].some(v=>v)));
check('embedded tilesets allow complete silent override audit',(tmj.tilesets??[]).every(t=>!t.source));
const objects=flattened.flatMap(l=>l.objects??[]);
const nativeAreas=objects.filter(o=>['area','zone'].includes(o.class));
const areas=Array.isArray(wam.areas)?wam.areas:[];
const unique=xs=>new Set(xs).size===xs.length;
check('unique WAM area IDs',unique(areas.map(a=>a.id)));
check('unique WAM area names',unique(areas.map(a=>a.name)));
check('unique WAM property IDs',unique(areas.flatMap(a=>(a.properties??[]).map(p=>p.id))));
check('unique TMJ area names',unique(nativeAreas.map(a=>a.name)));
const isRect=a=>['x','y','width','height'].every(k=>Number.isInteger(a[k]))&&a.width>0&&a.height>0&&!a.rotation&&!a.ellipse&&!a.polygon&&!a.polyline;
check('areas are positive integer aligned rectangles',[...areas,...nativeAreas].every(isRect));
check('all configured areas inside map world',[...areas,...nativeAreas].every(a=>a.x>=0&&a.y>=0&&a.x+a.width<=tmj.width*32&&a.y+a.height<=tmj.height*32));
const quiet=areas.filter(a=>a.properties?.some(p=>p.type==='silent'));
const nativeQuiet=nativeAreas.filter(a=>properties(a).silent===true);
const starts=areas.filter(a=>a.properties?.some(p=>p.type==='start'));
const defaults=starts.filter(a=>a.properties.some(p=>p.type==='start'&&p.isDefault===true));
const nativeStarts=nativeAreas.filter(a=>a.name==='start'||properties(a).start===true);
check('exactly one explicit default WAM start',defaults.length===1);
check('explicit default native TMJ start named start',nativeStarts.some(a=>a.name==='start'));
check('TMJ starts carry native class and boolean start property',nativeStarts.every(a=>['area','zone'].includes(a.class)&&properties(a).start===true));
check('all named starts support native 16px inset',[...starts,...nativeStarts].every(a=>a.width>=32&&a.height>=32));
const tuple=a=>[a.x,a.y,a.width,a.height].join(',');
check('default WAM and TMJ start geometry match',defaults.length===1&&nativeStarts.some(a=>a.name==='start'&&tuple(a)===tuple(defaults[0])));
check('WAM and native TMJ quiet unions mirror exactly',quiet.length===nativeQuiet.length&&quiet.every(q=>nativeQuiet.some(n=>tuple(n)===tuple(q))));
const overrides=[];
if('silent'in properties(tmj))overrides.push('map');
for(const l of flattened)if('silent'in properties(l))overrides.push('layer:'+l.name);
for(const o of objects)if('silent'in properties(o)&&(!nativeAreas.includes(o)||properties(o).silent!==true))overrides.push('object:'+o.name);
for(const t of tmj.tilesets??[])for(const tile of t.tiles??[])if('silent'in properties(tile))overrides.push('tile:'+t.name+':'+tile.id);
check('no competing map/layer/tile/false silence properties',overrides.length===0,{overrides});
check('WAM silence uses native presence-only property',quiet.every(a=>a.properties.filter(p=>p.type==='silent').every(p=>!('value'in p)&&!('enabled'in p))));
const inside=(p,a)=>p.x>=a.x&&p.x<=a.x+a.width&&p.y>=a.y&&p.y<=a.y+a.height;
const memberships=p=>({wamQuiet:quiet.filter(q=>inside(p,q)).map(q=>q.id),tmjQuiet:nativeQuiet.filter(q=>inside(p,q)).map(q=>q.name)});
const spawnCoverage=[];
for(const [kind,ss,margin] of [['WAM default',defaults,0],['WAM named',starts,16],['TMJ native',nativeStarts,16]])for(const a of ss){
 let count=0,missing=0,firstMissing=[];
 for(let y=a.y+margin;y<=a.y+a.height-margin;y++)for(let x=a.x+margin;x<=a.x+a.width-margin;x++){
  count++;const m=memberships({x,y:y+16});if(!m.wamQuiet.length||!m.tmjQuiet.length){missing++;if(firstMissing.length<3)firstMissing.push({x,y,feetY:y+16,...m});}
 }
 const row={kind,area:a.name,inset:margin,possibleIntegerSpawns:count,unprotectedSpawns:missing,firstMissing};spawnCoverage.push(row);
 check(kind+' complete inclusive random spawn footprint protected',count>0&&missing===0,row);
}

// Execute the retained StartPositionCalculator itself with a minimal map adapter.
// Type annotations are removed; runtime start selection and MathUtils are unchanged.
const mathJs=stripTypeScriptTypes(fs.readFileSync(path.join(source,'MathUtils.ts'),'utf8'),{mode:'transform'});
const mathUrl='data:text/javascript;base64,'+Buffer.from(mathJs).toString('base64');
let startJs=stripTypeScriptTypes(fs.readFileSync(path.join(source,'StartPositionCalculator.ts'),'utf8'),{mode:'transform'});
startJs=startJs.replace('import { GameMapProperties } from "@workadventure/map-editor";','const GameMapProperties={START:"start",START_LAYER:"startLayer"};').replace('"@workadventure/math-utils"',JSON.stringify(mathUrl));
const {StartPositionCalculator}=await import('data:text/javascript;base64,'+Buffer.from(startJs).toString('base64'));
function adapter(as){return {getAreas:()=>new Map(as.map(a=>[a.id,a])),getAreaByName:n=>as.find(a=>a.name===n),dynamicAreas:new Map(nativeAreas.map(a=>[a.name,{...a,properties:properties(a)}])),getFlatLayers:()=>flattened,hasStartTile:()=>false};}
function sample(as,name,random,init){const original=Math.random;Math.random=()=>random;try{return new StartPositionCalculator(adapter(as),tmj,init,name).startPosition;}finally{Math.random=original;}}
const startSamples=[];
for(const [label,as,name,a,inset]of [['WAM default',areas,undefined,defaults[0],0],['WAM named',areas,starts[0]?.name,starts[0],16],['TMJ fallback',[],undefined,nativeStarts.find(a=>a.name==='start'),16]])if(a){
 const low=sample(as,name,0),high=sample(as,name,0.999999),floatingPointHigh=sample(as,name,1-Number.EPSILON);startSamples.push({label,low,high,floatingPointHigh});
 check(label+' engine nominal runtime bounds match audited geometry',low.x===a.x+inset&&low.y===a.y+inset&&high.x===a.x+a.width-inset&&high.y===a.y+a.height-inset);
 // Math.random()*N + a positive coordinate can round upward at the highest
 // representable random values. Prove the conservative +1px fringe as well.
 let total=0,unprotected=0;
 for(let y=a.y+inset;y<=a.y+a.height-inset+1;y++)for(let x=a.x+inset;x<=a.x+a.width-inset+1;x++){
  total++;const m=memberships({x,y:y+16});if(!m.wamQuiet.length||!m.tmjQuiet.length)unprotected++;
 }
 check(label+' conservative floating-point fringe protected',unprotected===0,{possibleIntegerSpawnsIncludingFringe:total,unprotectedSpawns:unprotected,floatingPointHigh});
}
const rejoin=sample(areas,undefined,0,{x:23,y:47});
check('saved initPosition precedence verified',rejoin.x===23&&rejoin.y===47);

const socialPockets=[{name:'west social pocket',x:224,y:256,width:128,height:96},{name:'east social pocket',x:800,y:256,width:128,height:96}];
const socialObservations=socialPockets.map(a=>{
 const avatar={x:a.x+a.width/2,y:a.y+32},feet={x:avatar.x,y:avatar.y+16},m=memberships(feet);
 check(a.name+' interior anchor has no map-imposed silence',!m.wamQuiet.length&&!m.tmjQuiet.length,{avatar,feet,...m});
 const boundary=memberships({x:a.x+a.width/2,y:a.y+a.height});
 return {name:a.name,designRectangle:a,interiorAvatar:avatar,interiorFeet:feet,interiorOutsideConfiguredSilence:!m.wamQuiet.length&&!m.tmjQuiet.length,bottomBoundaryAtFeetY:a.y+a.height,bottomBoundary:boundary,claim:'Ordinary proximity intent only. These anchors are outside configured quiet zones; microphone/camera, proximity media, furniture seating, and two-user grouping are not runtime tested.'};
});
warnings.push('Social pocket bottom edge y=352 is inside the inclusive quiet-foyer boundary. Avatar centers at y>=336 place feet in that foyer. Do not label the entire social design rectangles unmuted.');
warnings.push('Default WAM start uses no inset. Named WAM/TMJ area starts use a 16px inset. Both area membership systems check avatar y+16 with inclusive rectangle edges.');
warnings.push('Exact runtime MathUtils sampling at Math.random()=1-Number.EPSILON can round the upper coordinate to max+1. The audit additionally covers the full conservative one-pixel right/bottom fringe.');
warnings.push('An explicit rejoin/initPosition overrides starts. Named URL starts can select another configured start. Initial socket grouping/media timing is not tested offline.');
warnings.push('Leaving map silence clears map-imposed silence only; saved busy/silent status, device permissions, and mute controls are not overridden. Silent zones are not a guarantee of all-audio silence.');
warnings.push('WAM silent handler toggles one area flag on enter/leave. Mirrored native TMJ quiet coverage is retained across adjoining quiet rectangles; live event ordering and media behavior remain untested.');
const report={checkedAt:new Date().toISOString(),sourceCommit:provenance.sourceCommit,scope:'Offline pinned-schema/migration, exact StartPositionCalculator execution with minimal map adapter, and complete integer spawn/quiet geometry audit. No server, multiplayer/media, room deployment, or portal destination verification.',wamPath,tmjPath,wamSha256:sha(raw),tmjSha256:sha(tmjRaw),checks,spawnCoverage,startSamples,socialObservations,warnings,allPassed:checks.every(c=>c.pass)};
fs.mkdirSync(path.dirname(reportPath),{recursive:true});fs.writeFileSync(reportPath,JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({reportPath,allPassed:report.allPassed,checks:checks.length,failedChecks:checks.filter(c=>!c.pass),spawnCoverage,socialObservations,warnings},null,2));
if(!report.allPassed)process.exitCode=1;
