// Executes the actual bundled fixture with mocked DOM / Phaser game boundaries.
// No browser rendering or full-app acceptance is implied.
const assert = require('node:assert/strict');
const vm = require('node:vm');
const { EventEmitter } = require('node:events');
const esbuild = require('./repo/node_modules/esbuild');
const source = require('fs').readFileSync(__dirname + '/fixture/fixture.js', 'utf8');
const filterExpression = source.match(/report\.filterEffectiveForTileLayers = ([^;]+);/)[1];
const filterEffective = new Function('mapName', 'linear', 'report', 'return ' + filterExpression);
for (const mapName of ['studio', 'reading', 'pixel-control']) for (const linear of [false, true]) for (const renderer of ['Canvas', 'WebGL']) assert.equal(filterEffective(mapName, linear, {renderer}), mapName !== 'pixel-control' && linear && renderer === 'WebGL');
console.log('12 actual-expression filter metadata cases passed, including nearest-only pixel-art control.');
const bundle = esbuild.buildSync({ entryPoints: [__dirname + '/fixture/fixture.js'], bundle: true, write: false, format: 'iife', platform: 'browser', target: 'es2020' }).outputFiles[0].text;
const elements = Object.fromEntries(Object.entries({ map:'studio',mode:'baseline',renderer:'canvas',zoom:'1',width:'1180',height:'757',offset:'0.25',stage:'',output:'',save:'',apply:'' }).map(([id,value])=>[id,{value,textContent:'',disabled:false,replaceChildren(){}}]));
const windowEvents = new EventEmitter();
const window = { devicePixelRatio:1, addEventListener:(n,f)=>windowEvents.on(n,f), removeEventListener:(n,f)=>windowEvents.off(n,f) };
const games = [];
class Game {
    constructor(config) { this.config=config;this.events=new EventEmitter();this.destroyRequested=false;games.push(this); }
    destroy() { this.destroyRequested=true; }
}
const context = {window,document:{getElementById:id=>elements[id],createElement:()=>({click(){}})},Phaser:{VERSION:'3.86.0',CANVAS:1,WEBGL:2,Core:{Events:{DESTROY:'destroy',PRE_RENDER:'prerender',POST_RENDER:'postrender'}},Game},console,performance,URL,Blob,setTimeout,clearTimeout};
vm.runInNewContext(bundle,context);
const settle=async()=>{for(let n=0;n<12;n++)await Promise.resolve();};
function preload(game) {const events={};const files=[];game.config.scene.preload.call({load:{on:(n,f)=>events[n]=f,tilemapTiledJSON:(k,p)=>files.push(p),image:(k,p)=>files.push(p),spritesheet:(k,p)=>files.push(p)}});return{events,files};}
(async()=>{
 let checks=0;
 await settle();assert.equal(games.length,1);checks++;
 const first=games[0],old=preload(first);assert(old.files.includes('assets/studio/map.tmj'));checks++;
 elements.mode.value='native';elements.mode.onchange();await settle();assert(first.destroyRequested);assert.equal(games.length,1);checks++;
 old.events.loaderror({url:'obsolete.png'});assert.equal(window.renderQualityFixture.report.status,'initializing');checks++;
 elements.map.value='reading';elements.map.onchange();elements.mode.value='native-linear';elements.mode.onchange();await settle();assert.equal(games.length,1);checks++;
 first.events.emit('destroy');await settle();assert.equal(games.length,2);assert.equal(window.renderQualityFixture.report.mapName,'reading');assert.equal(window.renderQualityFixture.report.mode,'native-linear');checks++;
 first.config.scene.create.call({get cameras(){throw Error('obsolete create ran');}});assert.equal(window.renderQualityFixture.report.status,'initializing');checks++;
 const second=games[1],current=preload(second);assert(current.files.includes('assets/reading/map.tmj'));assert(!current.files.includes('assets/studio/map.tmj'));checks++;
 second.config.scene.create.call({get cameras(){throw Error('expected create failure');}});assert.equal(window.renderQualityFixture.report.status,'failed');assert.equal(window.renderQualityFixture.report.failedStage,'scene-create');checks++;
 assert.equal(windowEvents.listenerCount('error'),1);assert.equal(windowEvents.listenerCount('unhandledrejection'),1);checks++;
 elements.mode.value='baseline';elements.mode.onchange();await settle();assert(second.destroyRequested);assert.equal(windowEvents.listenerCount('error'),0);assert.equal(games.length,2);checks++;
 second.events.emit('destroy');await settle();assert.equal(games.length,3);assert.equal(windowEvents.listenerCount('error'),1);checks++;
 windowEvents.emit('error',{message:'expected asynchronous failure'});assert.equal(window.renderQualityFixture.report.status,'failed');assert.equal(window.renderQualityFixture.report.failedStage,'asynchronous-runtime');checks++;
 console.log(checks+' actual-fixture lifecycle/async-error assertions passed with mocked DOM and Phaser Game boundaries; no browser rendering claim.');
})();
