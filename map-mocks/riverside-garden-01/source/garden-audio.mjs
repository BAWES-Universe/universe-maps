import {fireGainAtWorld,toWorld,feet} from './garden-geometry.mjs';
/** One bounded original loop; isolated preview only. No microphone, conversation or native room properties. */
export function createGardenAudio({onState=()=>{},AudioContext=globalThis.AudioContext,eventTarget=globalThis.window,documentTarget=globalThis.document,suspendMapSfxWhenHidden=false}={}){
 let context,master,gain,node,capture,pending,disposed=false,ready=false,muted=true,suspended=false,position=null,buffer;
 const abort=new AbortController();let sourceCount=0,lastGain=0;
 const state=()=>({ready,muted,suspended,disposed,gain:lastGain,sourceCount,contextState:context?.state??'not-created'});
 const reconcile=()=>{lastGain=fireGainAtWorld(position?toWorld(feet(position)):null,{ready,muted,suspended});if(context&&gain){const t=context.currentTime;gain.gain.cancelScheduledValues(t);gain.gain.setTargetAtTime(lastGain,t,.035);}onState(state());return state();};
 const api={
  async start(){if(disposed)throw Error('Audio preview is closed');if(ready){await context.resume();return reconcile();}if(pending)return pending;
   if(!AudioContext)throw Error('WebAudio is unavailable');
   if(!context){context=new AudioContext({latencyHint:'interactive'});master=context.createGain();gain=context.createGain();capture=context.createMediaStreamDestination();gain.gain.value=0;master.gain.value=1;gain.connect(master);master.connect(context.destination);master.connect(capture);}
   const resume=context.resume();
   pending=(async()=>{await resume;const response=await fetch(new URL('./audio/fire-gentle-original.mp3',import.meta.url),{signal:abort.signal});if(!response.ok)throw Error('Original crackle asset failed to load');buffer=await context.decodeAudioData(await response.arrayBuffer());if(disposed)return state();node=context.createBufferSource();node.buffer=buffer;node.loop=true;node.connect(gain);node.start();sourceCount++;ready=true;return reconcile();})().finally(()=>{pending=null;});return pending;
  },
  setPosition(p){position=p;return reconcile();},setMuted(v){muted=Boolean(v);return reconcile();},setSuspended(v){suspended=Boolean(v);return reconcile();},snapshot:state,getCaptureStream:()=>capture?.stream??null,
  dispose(){if(disposed)return;disposed=true;ready=false;abort.abort();try{node?.stop();}catch{}node?.disconnect();gain?.disconnect();master?.disconnect();if(context&&context.state!=='closed')void context.close();capture?.stream.getTracks().forEach(t=>t.stop());eventTarget?.removeEventListener('pagehide',hide);if(suspendMapSfxWhenHidden)documentTarget?.removeEventListener('visibilitychange',visibility);reconcile();}
 };
 const visibility=()=>api.setSuspended(documentTarget?.visibilityState==='hidden');const hide=()=>api.dispose();
 eventTarget?.addEventListener('pagehide',hide,{once:true});if(suspendMapSfxWhenHidden)documentTarget?.addEventListener('visibilitychange',visibility);
 return api;
}
