const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(process.argv[2]);
const p=root+'/celestial-transit-garden-calm-draft';
const N=require(root+'/tools/native/native-runtime-portable.cjs').createNative();
const w=new N.NativeWrapper();
const wam=JSON.parse(fs.readFileSync(p+'/map32/celestial-transit-garden-calm-draft.wam'));
const layout=JSON.parse(fs.readFileSync(p+'/source/layout.json'));
const routes=JSON.parse(fs.readFileSync(p+'/validation/native-routes.json'));
w.dynamicAreas=new Map(wam.areas.map(a=>[a.id,a]));
let entered=[];w.enterDynamicAreaCallbacks=[a=>entered.push(...a.map(v=>v.id))];w.leaveDynamicAreaCallbacks=[];
const rows=[];
for(const a of layout.areas){for(const leg of routes.rows.filter(r=>r.id==='spawn-to-'+a.id)){
 entered=[];const final={x:leg.final[0],y:leg.final[1]};
 w.triggerDynamicAreasChange({x:layout.start[0],y:layout.start[1]},final);
 const overlap=w.getDynamicAreasOnPosition(final).map(v=>v.id);
 rows.push({id:a.id,input:leg.input,final:leg.final,bodyBottomY:final.y+16,entered,overlap,pass:entered.includes(a.id)&&overlap.includes(a.id)});
}}
const distinct=new Set(rows.map(r=>r.id+'/'+r.input)).size;
const report={scope:'Independent direct execution of supplied pinned NativeWrapper dynamic-area entry methods using WAM areas and actual recorded native final coordinates. This does not test live Phaser event wiring or external destination services.',allPass:distinct===10&&rows.every(r=>r.pass),testCount:rows.length,uniqueDestinationInputPairs:distinct,rows};
console.log(JSON.stringify(report,null,2));if(!report.allPass)process.exitCode=1;
