import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { MapValidator } from '/workspace/shared/universe-audio-fix/libs/map-editor/src/GameMap/MapValidator';
import { WAMFileFormat } from '/workspace/shared/universe-audio-fix/libs/map-editor/src/types';
const root=path.resolve(__dirname,'..'),mapFile=path.join(root,'map/butterfly-campus.tmj');
const resources:any[]=[];
const validator=new MapValidator('info',{async fileExists(resource:string){const url=new URL(resource,pathToFileURL(mapFile));let exists=false;try{exists=url.protocol==='file:'&&fs.statSync(fileURLToPath(url)).isFile()}catch{}resources.push({resource,exists});return exists}});
async function main(){
 const result=await validator.validateStringMap(fs.readFileSync(mapFile,'utf8'));
 const wam=WAMFileFormat.safeParse(JSON.parse(fs.readFileSync(path.join(root,'integration/native-areas-proposal.wam'),'utf8')));
 const out={scope:'Unmodified MapValidator and WAMFileFormat from fork5e7670. Structural/resource/schema validation; no live media or full-Universe claim.',map:{ok:result.ok,...(!result.ok?{error:result.error}:{})},wam:{ok:wam.success,...(!wam.success?{error:wam.error.issues}:{areas:wam.data.areas.length})},resources};
 fs.writeFileSync(path.join(root,'evidence/native-contract-validation.json'),JSON.stringify(out,null,2));console.log(JSON.stringify(out));process.exitCode=result.ok&&wam.success?0:1;
}void main();
