// Isolated source-level harness of the installed plugin; not an actual-client animation capture.
const fs=require('fs'),path=require('path'),assert=require('assert');
global.Phaser={Plugins:{ScenePlugin:class{constructor(scene){this.scene=scene}}}};
const AnimatedTiles=require('/workspace/workadventure-universe/node_modules/phaser-animated-tiles');
const scene={sys:{settings:{isBooted:true}},time:{timeScale:1},events:{emit(){}}};
const plugin=new AnimatedTiles(scene,{}),tile={index:1};
const map={tilesets:[{firstgid:1,tileData:{0:{animation:[{tileid:0,duration:100},{tileid:1,duration:100},{tileid:2,duration:100}]}}}],layers:[{tilemapLayer:{type:'TilemapLayer'},data:[[tile]]}]};
plugin.init(map);plugin.active=true;
const sequence=[tile.index];for(let i=0;i<4;i++){plugin.postUpdate(0,101);sequence.push(tile.index)}
assert.deepStrictEqual(sequence,[1,2,3,1,2]);
// setTiles replaces index, then GameScene calls this exact method. It does not restart the clock.
tile.index=1;plugin.updateAnimatedTiles(0,0);const joinedPhase=tile.index;assert.equal(joinedPhase,2);
const report={method:'source-level harness using installed phaser-animated-tiles 2.0.2; no engine mutation',sequence,loopsAutomatically:true,resetTileToFirstFrame:1,actualIndexAfterUpdateAnimatedTiles:joinedPhase,joinsExistingPhase:true};
fs.writeFileSync(path.resolve(__dirname,'../../review/native-animation-capability.json'),JSON.stringify(report,null,2)+'\n');console.log(report);
