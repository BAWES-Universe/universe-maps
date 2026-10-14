import json,pathlib,collections,sys
r=pathlib.Path(__file__).resolve().parents[1];j=json.loads((r/sys.argv[1]/'source/layout.json').read_text());g=j['grid'];q=collections.deque([(j['start'][0]//32,j['start'][1]//32)]);v=set()
while q:
 x,y=q.popleft()
 if (x,y) in v or not(0<=x<48 and 0<=y<32) or g[y][x]:continue
 v.add((x,y));q.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
print([(x,y) for y in range(32) for x in range(48) if not g[y][x] and (x,y) not in v])
