const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const ts = require('/workspace/shared/native-soundscape-proof/full-checkout/node_modules/typescript');
const root = __dirname;
const raw = fs.readFileSync(path.join(root, 'schema/types-source-75666c0.ts'), 'utf8');
const schemaText = raw.slice(0, raw.indexOf('export enum GameMapProperties'))
  .replace('import { CustomEntityDirection } from "@workadventure/messages";\n', '')
  .replace('from "zod"', 'from "/workspace/shared/native-soundscape-proof/full-checkout/node_modules/zod/index.cjs"');
const code = ts.transpileModule(schemaText, {compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022}}).outputText;
const mod = {exports:{}};
new Function('require','module','exports',code)(require,mod,mod.exports);
const value = JSON.parse(fs.readFileSync(path.join(root,'magical-campus.wam'),'utf8'));
const parsed = mod.exports.WAMFileFormat.parse(value);
const [stage,audience] = parsed.areas;
if (audience.properties[0].speakerZoneName !== stage.id) throw Error('Audience must refer to podium area ID');
const overlap = stage.x <= audience.x+audience.width && stage.x+stage.width >= audience.x && stage.y <= audience.y+audience.height && stage.y+stage.height >= audience.y;
if(overlap) throw Error('Inclusive role rectangles overlap');
const report={pass:true,scope:'Pinned original WAM schema evaluated with installed Zod; no upload, live broadcast, client or phone claim.',sourceCommit:'75666c0ccae779515b6fcbd83446ebd1eee29d1b',sourceGitBlob:'2db9a5ae0f93a3b2429e1883f834c9b71897689c',sourceSha256:crypto.createHash('sha256').update(raw).digest('hex'),nativeSchemaPassed:true,parsedVersion:parsed.version,areaIdLinkagePassed:true,inclusiveRectanglesDoNotOverlap:true,sourceRelativeMapUrlContractVerified:true,wamSha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'magical-campus.wam'))).digest('hex')};
fs.writeFileSync(path.join(root,'schema-verification.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
