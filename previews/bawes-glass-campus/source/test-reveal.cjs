const {readFileSync}=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
(async()=>{
  for(const [position,initial] of [[{x:720,y:976},'show'],[{x:720,y:416},'hide'],[{x:720,y:304},'hide'],[{x:720,y:112},'show']]){
    const calls=[],handlers={};
    const WA={onInit:async()=>{},player:{getPosition:async()=>position},room:{
      hideLayer:name=>calls.push(['hide',name]),showLayer:name=>calls.push(['show',name]),
      onEnterLayer:name=>({subscribe:f=>handlers.enter=f}),onLeaveLayer:name=>({subscribe:f=>handlers.leave=f})
    }};
    await vm.runInNewContext(readFileSync(require('node:path').join(__dirname,'../runtime.js'),'utf8'),{WA,console});
    assert.deepEqual(calls,[[initial,'tower-glass-cover']]);
    for(let i=0;i<4;i++){handlers.enter();handlers.leave();}
    assert.equal(calls.length,9);
    assert.ok(calls.every(([,name])=>name==='tower-glass-cover'));
  }
  console.log('PASS: mocked outside/inside initialization and four reveal cycles; permanent collision never hidden. Not a game-runtime test.');
})().catch(e=>{console.error(e);process.exitCode=1});
