"""Pixel/source tests for the NEW revision06 geometry reconstruction.
Run: python test_geometry_patch.py [--source /path/to/restored/map16] [--greg /path/to/greg.png]
"""
import argparse
from collections import deque
import hashlib
import heapq
import json
import math
from pathlib import Path
import sys
import unittest
from PIL import Image, ImageDraw, ImageChops
from geometry_patch import *

parser=argparse.ArgumentParser()
parser.add_argument('--source',default='/workspace/shared/recovered-campus06/public/butterfly-town/v6/map16')
parser.add_argument('--patched',help='Optional integrated output map16/runtime directory to verify')
parser.add_argument('--greg',default='/workspace/shared/recovered-original-assets/map-mocks/civic-rooms-01/source/assets/greg.png')
args,extra=parser.parse_known_args()
SOURCE=Path(args.source); WORK=Path(__file__).parent
ORIGINAL=json.loads((SOURCE/'magical-campus.tmj').read_text()); PATCHED=apply_to_map(ORIGINAL)
if args.patched:
    integrated=json.loads(map_path(args.patched).read_text());il={l['name']:l for l in integrated['layers']};el={l['name']:l for l in PATCHED['layers']}
    for layer_name in ['collision-permanent','fixed-foreground','base']:
        assert il[layer_name]['data']==el[layer_name]['data'],f'Integrated output differs in {layer_name}'
    print('Integrated output geometry matches the tested patch; unrelated roof metadata permitted.')
W=ORIGINAL['width']; H=ORIGINAL['height']
OL={l['name']:l for l in ORIGINAL['layers']}; PL={l['name']:l for l in PATCHED['layers']}
SETS=ORIGINAL['tilesets']; ATLAS={t['firstgid']:Image.open(SOURCE/t['image']).convert('RGBA') for t in SETS}

def tile(gid):
    t=next(t for t in reversed(SETS) if t['firstgid']<=gid)
    n=gid-t['firstgid']; x=n%t['columns']*16; y=n//t['columns']*16
    return ATLAS[t['firstgid']].crop((x,y,x+16,y+16))

def render(layer):
    im=Image.new('RGBA',(W*16,H*16))
    for i,gid in enumerate(layer['data']):
        if gid:im.alpha_composite(tile(gid),(i%W*16,i//W*16))
    return im

BASE=render(OL['base']); BEFORE=render(OL['fixed-foreground']); AFTER=BEFORE.copy()
for x,y in BELOW_PLAYER_FASCIA_CELLS:AFTER.paste((0,0,0,0),(x*16,y*16,x*16+16,y*16+16))

def solid(data,x,y):
    return x<0 or y<0 or x>=W or y>=H or bool(data[y*W+x])

def body_clear(data,px,py):
    # Open intervals at right/bottom preserve exact native touching contact.
    x0=math.floor((px-8)/16); x1=math.floor((px+8-1e-7)/16)
    y0=math.floor(py/16); y1=math.floor((py+16-1e-7)/16)
    return not any(solid(data,x,y) for y in range(y0,y1+1) for x in range(x0,x1+1))

def cell_path(start,goal,data):
    # A bounded local search prevents a bad ring from silently going around the
    # other side of the fountain to reach the next clockwise waypoint.
    x0=min(start[0],goal[0])-2;x1=max(start[0],goal[0])+2
    y0=min(start[1],goal[1])-2;y1=max(start[1],goal[1])+2
    prev={start:None};costs={start:0};q=[(0,start)]
    while q:
        cost,(x,y)=heapq.heappop(q)
        if cost>costs[(x,y)]:continue
        if (x,y)==goal:break
        for dx,dy in [(1,1),(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1),(-1,-1)]:
            n=(x+dx,y+dy)
            if not(x0<=n[0]<=x1 and y0<=n[1]<=y1) or solid(data,*n):continue
            if dx and dy and (solid(data,x+dx,y) or solid(data,x,y+dy)):continue
            new_cost=cost+math.hypot(dx,dy)
            if new_cost>=costs.get(n,float('inf')):continue
            costs[n]=new_cost;prev[n]=(x,y);heapq.heappush(q,(new_cost,n))
    if goal not in prev:raise AssertionError(f'No local body-safe route {start} -> {goal}')
    result=[];p=goal
    while p is not None:result.append(p);p=prev[p]
    return result[::-1]

WAYPOINTS=[(90,108),(94,109),(97,111),(99,113),(100,114),(101,115),(101,117),(100,119),(98,121),(95,123),(91,124),(88,125),(85,124),(83,122),(81,120),(79,117),(79,114),(81,112),(83,110),(86,108),(90,108)]
ROUTE=[]
for a,b in zip(WAYPOINTS,WAYPOINTS[1:]):ROUTE+=cell_path(a,b,PL['collision-permanent']['data'])[:-1]
ROUTE.append(WAYPOINTS[-1])
PLAYER_ROUTE=[(x*16+8,y*16) for x,y in ROUTE]

class GeometryTests(unittest.TestCase):
    def test_exact_minimal_map_edits(self):
        expected={'collision-permanent':set(OPEN_FOUNTAIN_CELLS),'fixed-foreground':set(BELOW_PLAYER_FASCIA_CELLS)}
        for a,b in zip(ORIGINAL['layers'],PATCHED['layers']):
            if a['type']!='tilelayer':self.assertEqual(a,b);continue
            diff={(i%W,i//W) for i,(u,v) in enumerate(zip(a['data'],b['data'])) if u!=v}
            self.assertEqual(diff,expected.get(a['name'],set()))
            self.assertEqual({k:v for k,v in a.items() if k!='data'},{k:v for k,v in b.items() if k!='data'})
        self.assertEqual({k:v for k,v in ORIGINAL.items() if k!='layers'},{k:v for k,v in PATCHED.items() if k!='layers'})
        self.assertEqual(apply_to_map(PATCHED),PATCHED)
        self.assertNotEqual(ORIGINAL,PATCHED)

    def test_ring_swept_16px_body_both_directions(self):
        data=PL['collision-permanent']['data']; checks=0
        self.assertIn(((100,114),(101,115)),list(zip(ROUTE,ROUTE[1:])))
        self.assertGreater(sum(a[0]!=b[0] and a[1]!=b[1] for a,b in zip(ROUTE,ROUTE[1:])),10)
        for path in (PLAYER_ROUTE,PLAYER_ROUTE[::-1]):
            for a,b in zip(path,path[1:]):
                # Half-pixel swept steps are stricter than tile-center reachability.
                steps=math.ceil(max(abs(a[0]-b[0]),abs(a[1]-b[1]))*2)
                for k in range(steps+1):
                    px=a[0]+(b[0]-a[0])*k/steps;py=a[1]+(b[1]-a[1])*k/steps
                    self.assertTrue(body_clear(data,px,py),(px,py));checks+=1
        angle=0
        for a,b in zip(PLAYER_ROUTE,PLAYER_ROUTE[1:]):
            aa=math.atan2(a[1]+8-1871,a[0]-1448);bb=math.atan2(b[1]+8-1871,b[0]-1448)
            angle+=(bb-aa+math.pi)%(2*math.pi)-math.pi
        self.assertAlmostEqual(abs(angle),2*math.pi,places=7)
        self.assertGreater(checks,2000)

    def test_original_pinch_and_each_connector_are_required(self):
        original=OL['collision-permanent']['data'];self.assertFalse(body_clear(original,1616,1832))
        for cell in OPEN_FOUNTAIN_CELLS:
            data=PL['collision-permanent']['data'].copy();data[cell[1]*W+cell[0]]=61154
            self.assertFalse(body_clear(data,1616,1832),cell)
        # The planter edge is explicitly kept solid, as are every other basin,
        # pot, bench, and greenery tile in the original collision layer.
        self.assertEqual(PL['collision-permanent']['data'][116*W+100],61154)

    def test_removed_foreground_is_identical_native_base(self):
        count=0
        for x,y in BELOW_PLAYER_FASCIA_CELLS:
            for py in range(y*16,y*16+16):
                for px in range(x*16,x*16+16):
                    foreground=BEFORE.getpixel((px,py))
                    if foreground[3]:self.assertEqual(foreground,BASE.getpixel((px,py)));count+=1
        self.assertEqual(count,2304)
        pre=BASE.copy();pre.alpha_composite(BEFORE)
        post=BASE.copy();post.alpha_composite(AFTER)
        self.assertIsNone(ImageChops.difference(pre,post).getbbox())

    def test_contact_frontage_preserves_full_32px_bbox_all_frames(self):
        greg=Image.open(args.greg).convert('RGBA');self.assertEqual(greg.size,(96,128))
        frames=[greg.crop((x*32,y*32,(x+1)*32,(y+1)*32)) for y in range(4) for x in range(3)]
        self.assertEqual(len(frames),12)
        for route in CONTACT_ROUTES:
            x0,x1=route['centerX'];y0,y1=route['bodyTopY']
            # This whole native 32x32 sprite envelope is clear for every integer
            # position in the contact/frontage rectangle. It covers every alpha
            # pixel in all 12 Greg frames, and any other native 32px Woka frame.
            rect=(x0-16,y0-16,x1+16,y1+16)
            self.assertIsNone(AFTER.getchannel('A').crop(rect).getbbox(),route['id'])
            self.assertIsNotNone(BEFORE.getchannel('A').crop(rect).getbbox(),route['id'])
            for y in range(y0,y1+1):
                for x in range(x0,x1+1):self.assertTrue(body_clear(PL['collision-permanent']['data'],x,y))
            for cy in range(y0//16-1,(y1+16)//16+1):
                for cx in range((x0-16)//16,(x1+16)//16):
                    for layer in PATCHED['layers']:
                        if layer['type']=='tilelayer' and layer['name'].startswith('roof'):
                            self.assertEqual(layer['data'][cy*W+cx],0)

    def test_side_foliage_foreground_unchanged(self):
        for x in [171,172,183,184,195,196,197]:
            for y in range(178,191):
                i=y*W+x;self.assertEqual(OL['fixed-foreground']['data'][i],PL['fixed-foreground']['data'][i])
        # The collision test above separately requires no market collision edit.

if __name__=='__main__':
    (WORK/'ring-route.json').write_text(json.dumps({'status':'NEW reconstruction route','body':[-8,0,16,16],'playerPoints':PLAYER_ROUTE,'tilePoints':ROUTE,'waypoints':WAYPOINTS},indent=2)+'\n')
    unittest.main(argv=[sys.argv[0],*extra],verbosity=2)
