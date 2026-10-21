import {defineConfig} from 'vite';
import {getMaps,getMapsScripts,getMapsOptimizers} from 'wa-map-optimizer-vite';
import {readFileSync,writeFileSync,copyFileSync} from 'node:fs';
const maps=getMaps('.');
export default defineConfig({base:'./',build:{outDir:'dist',rollupOptions:{input:getMapsScripts(maps)}},plugins:[
 ...getMapsOptimizers(maps,{tile:{size:16}}),
 {name:'preserve-universe-runtime',closeBundle:{order:'post',sequential:true,handler(){
  const m=JSON.parse(readFileSync('dist/campus.tmj','utf8'));
  m.properties.find(p=>p.name==='script').value='runtime.js';
  writeFileSync('dist/campus.tmj',JSON.stringify(m));
  for(const name of ['runtime.js','index.html','PUBLICATION.json'])copyFileSync(name,'dist/'+name);
 }}}
]});
