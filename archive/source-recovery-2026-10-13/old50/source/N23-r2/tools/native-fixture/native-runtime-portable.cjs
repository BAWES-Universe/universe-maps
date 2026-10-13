// Portable runner for the source-extracted, pinned native methods. No engine dependencies.
const fs=require('node:fs'),vm=require('node:vm');
const compiled=fs.readFileSync(__dirname+'/extracted-current-source.cjs','utf8');
class Scheduler{
 constructor(){this.now=0;this.next=1;this.queue=new Map();this.executed=0;this.maxQueued=0;}
 set=(fn,delay=0)=>{const id=this.next++;this.queue.set(id,{id,fn,at:this.now+delay});this.maxQueued=Math.max(this.maxQueued,this.queue.size);return id};
 clear=(id)=>this.queue.delete(id);
 async flush(){for(let z=0;z<12;z++)await Promise.resolve();let steps=0;while(this.queue.size){if(++steps>1000)throw Error('Timer queue failed to settle');const t=[...this.queue.values()].sort((a,b)=>a.at-b.at||a.id-b.id)[0];this.queue.delete(t.id);this.now=Math.max(this.now,t.at);t.fn();this.executed++;for(let z=0;z<12;z++)await Promise.resolve();}for(let z=0;z<12;z++)await Promise.resolve();}
}
function createNative(){const scheduler=new Scheduler(),warnings=[];const globals={exports:{},setTimeout:scheduler.set,clearTimeout:scheduler.clear,Date:class extends Date{static now(){return scheduler.now}},console:{log(){},warn:(...v)=>warnings.push(v.join(' ')),error:(...v)=>warnings.push(v.join(' '))},CHARACTER_BODY_HEIGHT:16,CHARACTER_BODY_OFFSET_X:0,CHARACTER_BODY_OFFSET_Y:8,WOKA_SPEED:9,hasMovedEventName:'hasMoved',PositionMessage_Direction:{DOWN:0,LEFT:1,RIGHT:2,UP:3},passStatusToOnline(){},GameMapProperties:{COLLIDES:'collides',EXIT_URL:'exitUrl',EXIT_SCENE_URL:'exitSceneUrl',START:'start',START_LAYER:'startLayer'},get:x=>x,mapEditorToolbarInUseStore:false,botEditorToolActiveStore:false,isActivatable:()=>false,isQuickTap:p=>p.getDuration()<250,toggleMyCard(){},localUserStore:{getLocalUser:()=>({})},Player:class{},RemotePlayer:class{},CameraMode:{Focus:'focus'},CameraManagerEvent:{CameraUpdate:'update'},Easing:{SineEaseOut:'sine'}};
const context=vm.createContext(globals);context.window=context;vm.runInContext(fs.readFileSync(__dirname+'/easystar-0.4.4.js','utf8'),context);vm.runInContext(compiled,context);context.MathUtils=context.classes.NativeMath;return{...context.classes,scheduler,warnings,context};}
module.exports={createNative};
