const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),layout=JSON.parse(fs.readFileSync(root+'/source/layout.json'));
(async()=>{
for(const room of layout.buildings){
 const calls=[],handlers={};const [x,y,w,h]=room.interior;
 const WA={onInit:async()=>{},player:{getPosition:async()=>({x:(x+w/2)*32,y:(y+h/2)*32}),uuid:'test',onPlayerMove:()=>{}},state:{loadVariable:()=>false,onVariableChange:()=>({subscribe:()=>{}})},ui:{actionBar:{removeButton:()=>{},addButton:()=>{}}},room:{hideLayer:n=>calls.push(['hide',n]),showLayer:n=>calls.push(['show',n]),onEnterLayer:n=>({subscribe:f=>handlers[n+'enter']=f}),onLeaveLayer:n=>({subscribe:f=>handlers[n+'leave']=f})}};
 await vm.runInNewContext(fs.readFileSync(root+'/runtime.js','utf8'),{WA,console,setInterval:()=>0,Date,Map});
 assert(calls.some(([op,n])=>op==='hide'&&n===room.name+'-glass-cover'));
 handlers[room.name+'-interiorleave']();assert.deepEqual(calls.at(-1),['show',room.name+'-glass-cover']);
 assert(!calls.some(([,n])=>n==='persistent-collision'));
}
console.log('PASS: four complete shell initializations and leave handlers; permanent collision never hidden. Mocked API only.');
})().catch(e=>{console.error(e);process.exitCode=1});
