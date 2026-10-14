const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const esbuild=require('/workspace/shared/lantern-pr-work/repo/node_modules/esbuild');
const root=path.resolve(__dirname,'..'),source='/workspace/shared/universe-audio-fix';
const files=['libs/map-editor/src/GameMap/MapValidator.ts','libs/map-editor/src/types.ts'];
const provenance={sourceCommit:'5e7670be6c79efc575a7193e8a1a1c8c379b293f',sourceModification:'None',files:files.map(file=>({path:file,sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(source,file))).digest('hex')})),protobufAdapter:'Exact CustomEntityDirection enum adapter from prior source-verified validator setup; unrelated to the tested schemas.'};
esbuild.buildSync({entryPoints:[path.join(__dirname,'validate-contract.ts')],outfile:path.join(__dirname,'validate-contract.cjs'),bundle:true,platform:'node',format:'cjs',target:'node18',nodePaths:['/workspace/shared/lantern-pr-work/repo/node_modules'],alias:{'@workadventure/messages':'/workspace/shared/lantern-pr-work/engine-validation/custom-entity-direction-adapter.mjs'}});
fs.writeFileSync(path.join(root,'evidence/native-validator-provenance.json'),JSON.stringify(provenance,null,2));
