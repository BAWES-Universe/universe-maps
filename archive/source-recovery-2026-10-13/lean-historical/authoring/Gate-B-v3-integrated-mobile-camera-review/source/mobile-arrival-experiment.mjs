/* Experimental portrait arrival using existing APIs only.
 * The script iframe is hidden: never use its innerWidth or width media queries.
 * Device classification uses coarse pointer and Screen Orientation when available.
 * Authored overview dimensions are world coordinates, not a claimed viewport query.
 */
export function installMobileArrivalExperiment(WA,host=window,overview={width:640,height:1280}){
 const state={phase:'skipped',commands:0};
 const coarse=host.matchMedia('(pointer: coarse)').matches;
 const orientationType=host.screen?.orientation?.type;
 const portrait=typeof orientationType==='string' ? orientationType.startsWith('portrait') :
   Number.isFinite(host.orientation) ? Math.abs(host.orientation)%180===0 : host.screen.width<host.screen.height;
 state.device={coarse,portrait,orientationSource:typeof orientationType==='string'?'screen.orientation.type':Number.isFinite(host.orientation)?'legacy-window-orientation':'screen-aspect-heuristic'};
 const portraitCoarse=coarse && portrait;
 const empty=()=>({state,ready:Promise.resolve(),dispose(){}});
 if(!portraitCoarse||host.matchMedia('(prefers-reduced-motion: reduce)').matches||typeof WA?.camera?.set!=='function'||typeof WA?.camera?.followPlayer!=='function'||typeof WA?.player?.getPosition!=='function')return empty();
 let disposed=false,origin=null,latest=null;
 state.phase='waiting-for-position';
 const subscription=WA.player.onPlayerMove(position=>{
   if(disposed||!Number.isFinite(position?.x)||!Number.isFinite(position?.y))return;
   latest={x:position.x,y:position.y};
   if(state.phase!=='establishing')return;
   if(host.matchMedia('(prefers-reduced-motion: reduce)').matches){state.phase='motion-disabled';return;}
   if(position.y>origin.y-128)return;
   state.phase='walking';state.commands++;
   WA.camera.followPlayer(true,400);
 });
 const ready=WA.player.getPosition().then(position=>{
   if(disposed)return;
   if(host.matchMedia('(prefers-reduced-motion: reduce)').matches){state.phase='skipped';state.reason='reduced-motion';return;}
   const start=latest??position;
   // Late loading or joining at the gate must not drag the camera back to spawn.
   if(!Number.isFinite(start?.x)||!Number.isFinite(start?.y)||start.y<1056||start.x<352||start.x>608){state.phase='skipped';state.reason='already-away-from-arrival';return;}
   origin={...start};state.phase='establishing';state.commands++;
   WA.camera.set(480,800,overview.width,overview.height,false,false);
 }).catch(()=>{state.phase='skipped';state.reason='position-unavailable';});
 return{state,ready,dispose(){disposed=true;subscription.unsubscribe?.();}};
}
