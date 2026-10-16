// Assemble native-scale source-art crops into a world-aligned map atlas.
// The source images are never changed.90x54 is the measured court paving module.
const sharp=require('/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
module.exports=async root=>{
 const stone=await sharp(root+'/hub.png').extract({left:40,top:275,width:48,height:32}).resize(90,54).png().toBuffer();
 const groutX=await sharp(root+'/hub.png').extract({left:120,top:209,width:2,height:54}).png().toBuffer(),groutY=await sharp(root+'/hub.png').extract({left:32,top:261,width:90,height:2}).png().toBuffer();
 const tile=await sharp(stone).composite([{input:groutX,left:88,top:0},{input:groutY,left:0,top:52}]).png().toBuffer();
 const pieces=[];for(let y=-45;y<864;y+=54)for(let x=-42;x<1440;x+=90){const left=Math.max(0,x),top=Math.max(0,y),w=Math.min(1440,x+90)-left,h=Math.min(864,y+54)-top;if(w>0&&h>0)pieces.push({input:await sharp(tile).extract({left:left-x,top:top-y,width:w,height:h}).png().toBuffer(),left,top});}
 await sharp({create:{width:1440,height:864,channels:4,background:'#f3e7ce'}}).composite(pieces).png().toFile(root+'/bridge-surface.png');
 // A real court mosaic course, including its surrounding stone, defines the
 // landing inside the bridge. It does not paint over island or hub borders.
 await sharp(root+'/hub.png').extract({left:144,top:16,width:64,height:32}).png().toFile(root+'/threshold.png');
};
