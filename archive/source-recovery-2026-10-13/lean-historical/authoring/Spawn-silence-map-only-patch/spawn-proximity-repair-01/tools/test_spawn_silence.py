import copy,json,unittest
from pathlib import Path
from spawn_silence import audit,apply,starts
R=Path(__file__).resolve().parents[1]
class SpawnSilenceTests(unittest.TestCase):
 def setUp(self):self.baseline=json.loads((R/'fixtures/campus09-original.tmj').read_text())
 def test_missing_protection_fails(self):self.assertFalse(audit(self.baseline)['allSpawnsProtected'])
 def test_nonstandard_grid_is_rejected(self):
  m=copy.deepcopy(self.baseline);m['tilewidth']=m['tileheight']=16
  with self.assertRaisesRegex(ValueError,'32px'):audit(m)
 def test_unresolved_external_tileset_is_rejected(self):
  m=copy.deepcopy(self.baseline);m['tilesets']=[{'firstgid':1,'source':'unresolved.tsj'}]
  with self.assertRaisesRegex(ValueError,'External tilesets'):audit(m)
 def test_32px_spawn_bottom_edge_is_inclusive(self):
  m=copy.deepcopy(self.baseline);o=next(o for l in m['layers']for o in l.get('objects',[])if o.get('name')=='start');o['properties'].append({'name':'silent','type':'bool','value':True});self.assertEqual(starts(m)[0]['footpoints'],[(936,1584)]);self.assertTrue(audit(m)['allSpawnsProtected'])
 def test_all_randomized_template_spawns(self):
  m=json.loads((R/'fixtures/outdoor-office01-original.tmj').read_text());points=starts(m)[0]['footpoints'];self.assertEqual(len(points),65*33);self.assertEqual((min(p[0]for p in points),max(p[0]for p in points),min(p[1]for p in points),max(p[1]for p in points)),(464,528,704,736));self.assertTrue(audit(apply(m))['allSpawnsProtected'])
 def test_small_center_marker_does_not_cover_random_spawns(self):
  m=json.loads((R/'fixtures/outdoor-office01-original.tmj').read_text());n=apply(m);q=next(o for l in n['layers']for o in l.get('objects',[])if o.get('name','').startswith('spawn-quiet-'));q.update(x=488,y=704,width=16,height=16);self.assertFalse(audit(n)['allSpawnsProtected'])
 def test_exit_clears_area_membership_and_preserves_audio(self):
  m=apply(self.baseline);self.assertTrue(audit(m)['normalAreaStatusAfterExit']);old=[o for l in self.baseline['layers']for o in l.get('objects',[])if o.get('name','').startswith('ambient-')];new=[o for l in m['layers']for o in l.get('objects',[])if o.get('name','').startswith('ambient-')];self.assertEqual(old,new)
 def test_conflicting_layer_override_is_rejected(self):
  m=apply(self.baseline);m['layers'][0]['properties']=[{'name':'silent','type':'bool','value':False}];self.assertFalse(audit(m)['allSpawnsProtected'])
 def test_tiled_startlayer_cell_feet_are_covered(self):
  m={'width':4,'height':4,'tilewidth':32,'tileheight':32,'layers':[{'id':1,'type':'tilelayer','name':'start','width':4,'height':4,'data':[0]*5+[1]+[0]*10},{'id':2,'type':'objectgroup','name':'areas','objects':[]}],'nextobjectid':1};self.assertEqual(starts(m)[0]['footpoints'],[(48,64)]);self.assertTrue(audit(apply(m))['allSpawnsProtected'])
if __name__=='__main__':unittest.main()
