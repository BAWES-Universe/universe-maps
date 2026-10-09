const fs=require('node:fs');
const http=require('node:http');
const path=require('node:path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'..');
(async()=>{
 const server=http.createServer((req,res)=>{const rel=decodeURIComponent(new URL(req.url,'http://localhost').pathname);const file=path.join(root,rel==='/'?'index.html':rel);if(!file.startsWith(root)){res.writeHead(403);return res.end()}fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);return res.end()}const ext=path.extname(file);res.setHeader('Content-Type',({'.html':'text/html','.mjs':'text/javascript','.js':'text/javascript','.png':'image/png','.json':'application/json'})[ext]||'text/plain');res.end(data)})});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const browser=await chromium.launch({headless:true,executablePath:'/usr/bin/chromium'});const page=await browser.newPage({viewport:{width:1472,height:700},deviceScaleFactor:1});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:'+server.address().port);await page.waitForFunction(()=>document.querySelector('#position').textContent.includes('1504'));
 await page.screenshot({path:path.join(root,'docs/browser-native-arrival.png'),fullPage:true});
 const initial=await page.locator('#position').textContent();
 await page.keyboard.down('ArrowLeft');await page.waitForTimeout(1000);await page.keyboard.up('ArrowLeft');const leftWall=await page.locator('#position').textContent();
 await page.locator('#reset').click();await page.keyboard.down('ArrowUp');await page.waitForTimeout(1280);await page.keyboard.up('ArrowUp');await page.keyboard.down('ArrowLeft');await page.waitForTimeout(1000);await page.keyboard.up('ArrowLeft');const branch=await page.locator('#position').textContent();
 const canvas=await page.locator('canvas').evaluate(e=>({width:e.width,height:e.height,cssWidth:e.getBoundingClientRect().width,cssHeight:e.getBoundingClientRect().height}));
 const report={initial,leftWall,branch,canvas,pageErrors:errors,assertions:{initialArrival:initial.includes('1504, 2912'),lowerLeftGardenBlocks:leftWall.includes('1449')||leftWall.includes('1448'),branchMovesLeft:Number(branch.match(/World (\d+)/)?.[1])<1440,nativeCanvas:canvas.width===1472&&canvas.cssWidth===1472&&canvas.height===576&&canvas.cssHeight===576,noPageErrors:errors.length===0}};
 fs.writeFileSync(path.join(root,'docs/browser-verification.json'),JSON.stringify(report,null,2)+'\n');console.log(report);await browser.close();server.close();if(Object.values(report.assertions).some(x=>!x))process.exitCode=1;
})();
