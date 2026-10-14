const test=require('node:test'),assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const code=fs.readFileSync(require.resolve('../runtime/moonlit.js'),'utf8');
function setup(){
 const pending=new Map(),registered=new Map();let id=0,follow=0;
 const sandbox={module:{exports:{}},setTimeout:function(fn){'use strict';assert.equal(this,sandbox.globalRef,'native timer receiver');pending.set(++id,fn);return id},clearTimeout:function(id){'use strict';assert.equal(this,sandbox.globalRef,'native cancellation receiver');pending.delete(id)}};
 vm.createContext(sandbox);vm.runInContext('globalThis.globalRef=globalThis',sandbox);vm.runInContext(code,sandbox);
 const WA={room:{hashParameters:{},showLayer(){},hideLayer(){},setProperty(){}},state:{onVariableChange:()=>({subscribe:()=>({unsubscribe(){}})})},player:{getPosition:async()=>({x:448,y:704}),onPlayerMove:()=>({unsubscribe(){}})},camera:{set(){},followPlayer(){follow++}},ui:{registerMenuCommand(label,options){const key=options.key??('random-key-'+registered.size);registered.set(key,{label,options});return{remove:()=>registered.delete(key)}}}};
 return{app:sandbox.module.exports.createExperience(WA),pending,registered,follow:()=>follow};
}
test('default timer scheduling and cancellation retain browser-global receiver',async()=>{const m=setup();await m.app.init();m.app.viewTerrace();assert.equal(m.pending.size,1);m.app.viewTerrace();assert.equal(m.pending.size,1);for(const f of m.pending.values())f();assert.equal(m.follow(),1);m.app.dispose()});
test('native departure cleanup by descriptor removes every keyed menu; rejoin callbacks remain functional',async()=>{const m=setup();await m.app.init();assert.equal(m.registered.size,4);for(const {label} of [...m.registered.values()])m.registered.delete(label);assert.equal(m.registered.size,0);const n=setup();await n.app.init();assert.equal(n.registered.size,4);n.registered.get('View moon terrace').options.callback();assert.equal(n.pending.size,1);n.app.dispose();assert.equal(n.registered.size,0)});
