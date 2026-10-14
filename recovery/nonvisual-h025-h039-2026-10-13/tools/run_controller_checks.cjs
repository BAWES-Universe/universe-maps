'use strict';
// Execute retained author checks against the newly derived script.
// H039 has one raster-dependent case: record it BLOCKED without fabricating its
// missing state hashes. All other test bodies and WA mocks remain unchanged.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const mapid = process.argv[2];
if (!['H025', 'H039'].includes(mapid)) throw Error('Specify H025 or H039');
const out = path.resolve(process.argv[3] || path.join(root, 'generated'));
const filename = path.join(root, 'retained', mapid, 'tools/test-controller.cjs');
const context = { require, console, process, Buffer, setTimeout, clearTimeout,
  __dirname: path.join(out, mapid, 'tools'), __filename: filename };
let code = fs.readFileSync(filename, 'utf8');
if (mapid === 'H039') {
  const original = 'async function test(name,fn){await fn();cases.push({name,pass:true})}';
  const replacement = `async function test(name,fn){
    if(name==='64 unique decoded physical states and16 bounded overlays inside unchanged solids'){
      cases.push({name,pass:null,status:'BLOCKED',reason:'Original raster masters and rendered state/footprint reports remain missing.'});return;
    }
    await fn();cases.push({name,pass:true});
  }`;
  if (!code.includes(original) || !code.includes('allPass:true,cases')) throw Error('Retained test shape changed');
  code = code.replace(original, replacement).replace('allPass:true,cases',
    "allPass:false,allRunnableControllerChecksPass:true,missingArtCheckBlocked:true,cases");
}
vm.runInNewContext(code, context, {filename});
