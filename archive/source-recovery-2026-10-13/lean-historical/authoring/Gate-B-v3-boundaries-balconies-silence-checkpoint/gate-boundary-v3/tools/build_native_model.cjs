const fs=require('node:fs'),path=require('node:path'),{stripTypeScriptTypes}=require('node:module');const R=path.resolve(__dirname,'..'),D=path.join(R,'source-audit');
const source=n=>stripTypeScriptTypes(fs.readFileSync(path.join(D,n),'utf8'),{mode:'transform'});
function method(s,n){const start=s.search(new RegExp('^    (?:async )?'+n+'\\(','m'));if(start<0)throw Error(n);let pos=s.indexOf('{',start),end=pos,depth=1;while(depth){end++;if(s[end]==='{')depth++;if(s[end]==='}')depth--;}return s.slice(start,end+1).trim();}
const p=source('Player.ts'),methods=['setPathToFollow','getCurrentPathDestinationPoint','finishFollowingPath','deduceSpeed','adjustPathToFollowToColliderBounds','followPath','moveToPos'];
const header=`/* Current Universe 75666c0 exact source-extracted methods. Rendering, stores and networking are adapters; this is a model, not a live runtime. */
const EasyStar=globalThis.EasyStar,MathUtils={distanceBetween:(a,b,sqrt=true)=>sqrt?Math.hypot(a.x-b.x,a.y-b.y):(a.x-b.x)**2+(a.y-b.y)**2,isBetween:(n,min,max)=>n>=min&&n<=max};
const CHARACTER_BODY_HEIGHT=16,CHARACTER_BODY_OFFSET_X=0,CHARACTER_BODY_OFFSET_Y=8,WOKA_SPEED=9,hasMovedEventName='hasMoved',PositionMessage_Direction={DOWN:0,LEFT:1,RIGHT:2,UP:3},passStatusToOnline=()=>{};
`;
const player=`export class NativePathPlayer {constructor(x,y){this.x=x;this.y=y;this._lastDirection=3;this.currentPathSegmentDistanceFromStart=0;this.body={height:16,offset:{y:8},setDirectControl(v){this.directControl=v}};this.scene={markDirty(){}};this.events=[];}
getBody(){return this.body;}stop(){}setDepth(v){this.depth=v;}playAnimation(d,m){this.direction=d;this.moving=m;}emit(n,e){}
${methods.map(n=>method(p,n)).join('\n')}\n}\n`;
fs.writeFileSync(path.join(R,'validation/native-path-model.mjs'),header+source('PathfindingManager.ts').replace(/^import .*;\n/gm,'')+player);
console.log('Generated current pinned native model.');
