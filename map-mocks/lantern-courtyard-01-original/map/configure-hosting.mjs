#!/usr/bin/env node
// Offline-only URL binding. This script never connects, uploads, or changes a server.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const supplied=process.argv[2];
if(!supplied){console.error('Usage: node configure-hosting.mjs "https://YOUR-ASSET-HOST/NEW-ISOLATED-DIRECTORY/"\nUse the verified final asset directory URL, including its trailing slash. No files will be uploaded.');process.exit(2);}
let base;try{base=new URL(supplied);}catch{console.error('Enter a complete verified HTTPS asset-directory URL.');process.exit(2);}
if(base.protocol!=='https:'||base.username||base.password||base.search||base.hash||!base.pathname.endsWith('/')||base.pathname==='/'||/YOUR-|example\.|\.invalid$/i.test(base.hostname)){
 console.error('Refusing an insecure, root, credential-bearing, incomplete or placeholder URL. Use the verified HTTPS directory for this isolated proof.');process.exit(2);
}
const wamPath=path.join(root,'lantern-courtyard.wam');
const wam=JSON.parse(fs.readFileSync(wamPath,'utf8'));
wam.mapUrl=new URL('lantern-courtyard.tmj',base).href;
wam.entityCollections=[{url:new URL('collections/courtyard-furniture.json',base).href,type:'file'}];
fs.writeFileSync(wamPath,JSON.stringify(wam,null,2)+'\n');
fs.writeFileSync(path.join(root,'hosting-bound.json'),JSON.stringify({assetBaseUrl:base.href,mapUrl:wam.mapUrl,collectionUrl:wam.entityCollections[0].url,onlyLocalFilesChanged:true},null,2)+'\n');
console.log('Bound the local WAM to '+base.href+'\nNothing uploaded. Re-zip this directory contents, then use only the authorized NEW isolated upload directory.');
