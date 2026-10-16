const fs=require('fs'),root='/workspace/azure-expanded',centers=JSON.parse(fs.readFileSync(root+'/source/seat-art-centers.json'));
const areas={
cafe:{origin:[1952,64],floors:[[96,96,1024,864],[480,928,256,288]],solids:[[96,96,160,192],[960,96,160,192],[96,800,160,128],[960,800,160,128],[256,64,704,128]],tables:[[352,320,64,96],[800,320,64,96],[352,704,64,64],[800,704,64,64]]},
lounge:{origin:[64,1952],floors:[[96,128,1024,928],[1088,480,128,256]],solids:[[96,96,160,160],[960,96,160,160],[96,896,160,160],[960,896,160,160],[224,256,64,608],[256,256,512,64],[256,800,704,64]],tables:[[384,512,96,96],[704,512,96,96]]},
garden:{origin:[1952,3840],floors:[[96,96,1024,960],[480,0,256,128]],solids:[[96,96,128,160],[992,96,128,160],[96,928,128,128],[992,928,128,128],[256,256,192,224],[768,256,192,224],[256,736,192,192],[768,736,192,192],[512,512,192,192]],tables:[]},
gathering:{origin:[3840,1952],floors:[[96,128,1024,928],[0,480,128,256]],solids:[[128,128,160,160],[928,128,160,160],[128,864,160,160],[928,864,160,160]],tables:[[384,288,64,96],[768,288,64,96],[384,800,64,64],[768,800,64,64]]},
hub:{origin:[2176,2176],floors:[[0,0,768,768]],solids:[[32,32,96,96],[640,32,96,96],[32,608,96,96],[640,608,96,96],[288,256,192,224]],tables:[[192,96,64,64],[512,96,64,64],[192,576,64,64],[512,576,64,64]]}
};
let furniture=[],floors=[],seats=[];for(const[id,a]of Object.entries(areas)){const[ox,oy]=a.origin;for(const[x,y,w,h]of a.floors)floors.push([x+ox,y+oy,w,h]);for(const[kind,rs]of[['solid',a.solids],['table',a.tables]])for(const[x,y,w,h]of rs)furniture.push({island:id,kind,x:x+ox,y:y+oy,w,h});for(const [i,[x,y]]of centers[id].entries())seats.push({id:id+'-'+i,island:id,x:x+ox,y:y+oy,approachDistance:id==='lounge'&&i<3?16:32});}
const baySeats=[[2384,1712],[2736,1712],[2384,3376],[2736,3376],[1712,2384],[1712,2736],[3376,2384],[3376,2736]].map(([x,y],i)=>({id:'viewing-bay-'+i,island:'bridge',x,y,approachDistance:32}));seats.push(...baySeats);
fs.writeFileSync(root+'/source/art-geometry.json',JSON.stringify({areas,floors,furniture,seats,baySeats,notes:'Collision approximates visible artwork on native32px tile grid; full gameplay review pending.'},null,2));
