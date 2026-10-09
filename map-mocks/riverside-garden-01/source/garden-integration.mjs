import {fromWorld} from './garden-geometry.mjs';
/** Explicit caller-owned map-SFX integration. No global audio/microphone/video settings or listeners. */
export function createGardenIntegration(audio,{sceneId='magicalUniverse'}={}){
 let currentScene=null,worldPosition=null,userMuted=true,backgroundSuppressed=false,disposed=false;
 function sync(){const valid=worldPosition&&Number.isFinite(worldPosition.x)&&Number.isFinite(worldPosition.y);const active=currentScene===sceneId&&valid;
  // Suspend this source first so scene changes cannot briefly reuse an old position.
  audio.setSuspended(true);audio.setMuted(userMuted);audio.setPosition(valid?fromWorld(worldPosition):null);audio.setSuspended(!active||backgroundSuppressed);return snapshot();
 }
 function snapshot(){return {currentScene,worldPosition,active:currentScene===sceneId&&!backgroundSuppressed,userMuted,backgroundSuppressed,disposed,audio:audio.snapshot()};}
 return {
  handleRouteTransition({sceneId:nextScene,worldPosition:nextPosition}={}){if(disposed)return snapshot();currentScene=nextScene??null;worldPosition=nextPosition??null;return sync();},
  handleWorldPosition(p){if(disposed)return snapshot();worldPosition=p;return sync();},
  handleUserMute(muted){if(disposed)return snapshot();userMuted=Boolean(muted);return sync();},
  // Optional host signal for this map's SFX only. No document.visibilityState listener is installed here.
  handleMapSfxSuppression(value){if(disposed)return snapshot();backgroundSuppressed=Boolean(value);return sync();},
  async startFromUserGesture(){if(disposed)throw Error('Garden integration disposed');await audio.start();return sync();},
  snapshot,
  dispose(){if(disposed)return;disposed=true;audio.dispose();}
 };
}
