/* Butterfly Town · quiet by default. No independent audio output.
 * Candidate policy only: not loaded by the map until native audio is reviewed.
 * The earlier scored-town sketch is preserved as art, not a runtime plan.
 */
export const AUDIO_VERSION = 2;
export const AUDIO_ASSETS = Object.freeze({
  fountain:'assets/audio/fountain.mp3',
  crossing:'assets/audio/gate-crossing.mp3', // Optional and OFF by default.
});
const GATE={x:512,y:384,width:1024,height:1536};
const TOWN={x:2304,y:512,width:1536,height:1024};
export const FUNCTIONAL_SILENT_ZONES=Object.freeze([
  {id:'studenthub',x:2496,y:672,width:384,height:240},
  {id:'cafe',x:3328,y:704,width:320,height:240},
  {id:'archive',x:3360,y:1152,width:256,height:176},
]);
export const FOUNTAIN_SOURCE=Object.freeze({
  id:'fountain',kind:'fountain',url:AUDIO_ASSETS.fountain,scene:'town',
  center:{x:3072,y:991},innerRadius:56,outerRadius:144,maxGain:.35,
  bounds:{x:2928,y:847,width:288,height:288},edgeFade:32,
});
// No separately verified waterfall geometry or dedicated waterfall asset exists
// in this map revision. Do not mistake the portal's animated water ribbon for it.
export const WATERFALL_SOURCES=Object.freeze([]);
const cap=v=>Math.min(1,Math.max(0,v));
const smooth=v=>{const x=cap(v);return x*x*(3-2*x);};
const inside=(p,r)=>p.x>=r.x&&p.x<=r.x+r.width&&p.y+16>=r.y&&p.y+16<=r.y+r.height;
function validBounds(b){return b&&[b.x,b.y,b.width,b.height].every(Number.isFinite)&&b.width>0&&b.height>0;}
export function getLocalizedWaterGain(position,source){
  if(!position||!Number.isFinite(position.x)||!Number.isFinite(position.y)||
    !source||!validBounds(source.bounds)||!inside(position,source.bounds)||
    !source.center||!Number.isFinite(source.center.x)||!Number.isFinite(source.center.y)||
    !Number.isFinite(source.innerRadius)||source.innerRadius<0||!Number.isFinite(source.outerRadius)||
    source.outerRadius<=source.innerRadius||!Number.isFinite(source.maxGain)||
    !Number.isFinite(source.edgeFade)||source.edgeFade<=0)return 0;
  const footY=position.y+16,b=source.bounds;
  const distance=Math.hypot(position.x-source.center.x,footY-source.center.y);
  const radial=1-smooth((distance-source.innerRadius)/(source.outerRadius-source.innerRadius));
  const edge=Math.min(position.x-b.x,b.x+b.width-position.x,footY-b.y,b.y+b.height-footY);
  return Math.min(.35,Math.max(0,source.maxGain))*radial*smooth(edge/source.edgeFade);
}
export function getTownSoundscape(position,{waterfalls=WATERFALL_SOURCES,silentZones=[]}={}){
  const empty={scene:'silent',room:null,source:null,levels:{fountain:0,waterfall:0},reason:'outside-map'};
  if(!position||!Number.isFinite(position.x)||!Number.isFinite(position.y))return{...empty,reason:'invalid-position'};
  const scene=inside(position,TOWN)?'town':inside(position,GATE)?'gate':'silent';
  if(scene==='silent')return empty;
  // Silence takes precedence over proximity, optional cues and every water zone.
  const quiet=[...FUNCTIONAL_SILENT_ZONES,...silentZones].find(z=>validBounds(z)&&inside(position,z));
  if(quiet)return{...empty,scene,room:quiet.id??'functional-area',reason:'functional-area'};
  const candidates=[FOUNTAIN_SOURCE,...waterfalls].filter(s=>s&&s.scene===scene&&
    (s.kind==='fountain'||s.kind==='waterfall')&&typeof s.url==='string'&&s.url.length>0)
    .map(s=>({definition:s,gain:getLocalizedWaterGain(position,s)})).filter(s=>s.gain>0)
    .sort((a,b)=>b.gain-a.gain||String(a.definition.id).localeCompare(String(b.definition.id)));
  // One native source at a time: overlapping features cannot stack their levels.
  if(!candidates.length)return{...empty,scene,reason:'quiet-default'};
  const {definition:s,gain}=candidates[0];
  return{scene,room:null,reason:'localized-water',source:{id:s.id,kind:s.kind,url:s.url,volume:gain,loop:true},
    levels:{fountain:s.kind==='fountain'?gain:0,waterfall:s.kind==='waterfall'?gain:0}};
}

/* Adapter contract, NOT an available WA API or independent player:
 * setSource(url,{volume,loop}): existing native playAudio/audioVolume/audioLoop.
 * setVolume(volume): same-URL authored gain update without restarting playback.
 * silence(): unset playAudio to immediately unload BOTH native fade slots; preserve user controls.
 * playCue(id,gain): optional native-channel cue, never a separate WA.sound bypass.
 * stop(): cancel owned playback/work on disposal.
 * Host owns mute/pause/volume, gesture recovery and ducking. No custom controls.
 */
export class TownAudioDirector {
  constructor(adapter,{now=()=>performance.now(),waterfalls=WATERFALL_SOURCES,silentZones=[],enableGateCue=false}={}){
    this.adapter=adapter;this.now=now;this.policy={waterfalls,silentZones};this.enableGateCue=enableGateCue===true;
    this.disposed=false;this.hidden=false;this.last=null;this.lastSent=undefined;this.lastCue=-Infinity;this.crossingIds=new Set();
  }
  observe(position){if(this.disposed)return;this.last=getTownSoundscape(position,this.policy);this.flush();return this.last;}
  flush(){
    if(this.disposed||!this.last)return;
    const source=this.hidden?null:this.last.source;
    if(!source){if(this.lastSent!==null){this.adapter.silence();this.lastSent=null;}return;}
    if(this.lastSent?.url!==source.url){this.adapter.setSource(source.url,{volume:source.volume,loop:true});this.lastSent={...source};return;}
    // Subpixel movement does not spam source changes or restart water loops.
    if(Math.abs(source.volume-this.lastSent.volume)>=.005){this.adapter.setVolume(source.volume);this.lastSent={...source};}
  }
  gateCrossed(transitionId){
    if(this.disposed||this.last?.scene!=='town'||transitionId==null||this.crossingIds.has(transitionId))return false;
    this.crossingIds.add(transitionId);if(this.crossingIds.size>32)this.crossingIds.delete(this.crossingIds.values().next().value);
    // Skipped crossings are consumed: they must never replay after foregrounding.
    if(!this.enableGateCue||this.hidden||this.last.room||this.last.source)return false;
    const now=this.now();if(now-this.lastCue<4500)return false;
    this.lastCue=now;this.adapter.playCue('crossing',.12);return true;
  }
  setHidden(hidden){if(this.disposed)return;this.hidden=!!hidden;this.flush();}
  dispose(){if(this.disposed)return;this.disposed=true;this.adapter.stop();this.lastSent=null;this.crossingIds.clear();}
}
