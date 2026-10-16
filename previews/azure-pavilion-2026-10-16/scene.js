(async function(){'use strict';await WA.onInit();let position=await WA.player.getPosition(),inside=false,popup=null,sound=null,playing=false,busy=false;
const seats=[{x:416,y:272,side:-1},{x:512,y:272,side:1},{x:768,y:272,side:-1},{x:864,y:272,side:1},{x:576,y:880,side:-1},{x:704,y:880,side:1}];
function roof(p){position=p;const next=p.x>352&&p.x<928&&p.y+16<400&&p.y+16>160;if(next!==inside){inside=next;WA.room[next?'hideLayer':'showLayer']('Glass canopy');}}
roof(position);WA.player.onPlayerMove(roof);
function close(){if(popup)popup.close();popup=null;}
function controls(){close();popup=WA.ui.openPopup('actions-'+Math.max(0,Math.min(2,Math.round((position.y+16-272)/256)))+'-'+Math.max(0,Math.min(2,Math.round((position.x-320)/320))),'Azure Pavilion\nSea breeze is optional. Choose Play to hear it.',[{label:playing?'Stop sea sound':'Play sea sound',className:playing?'warning':'primary',callback:()=>{if(playing){sound.stop();playing=false;}else{sound=sound||WA.sound.loadSound('sea-breeze.wav');sound.play({loop:true,volume:.45});playing=true;}close();}},{label:'Close',className:'normal',callback:close}]);}
WA.ui.registerMenuCommand('Pavilion sound',controls);
WA.ui.registerMenuCommand('Take nearest seat',async()=>{if(busy)return;const s=seats.reduce((a,b)=>Math.hypot(position.x-a.x,position.y+16-a.y)<Math.hypot(position.x-b.x,position.y+16-b.y)?a:b);if(Math.hypot(position.x-s.x,position.y+16-s.y)>112)return;busy=true;try{const r=await WA.player.moveTo(s.x+s.side*32,s.y,3);if(!r.cancelled)await WA.player.moveTo(s.x,s.y,3);}finally{busy=false;}});
})();
