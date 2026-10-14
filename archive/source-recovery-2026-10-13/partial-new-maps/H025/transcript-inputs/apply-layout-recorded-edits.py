from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'transcript-inputs/author-layout.initial.py').read_text()
# Exact sequential replacement strings retained in the original tool-call inputs.
s=s.replace('anchor=[936,735]','anchor=[936,719]').replace('[29,22],[29,23]','[29,22]').replace('656,304,24','656,303,24').replace('rect([1118,417,1175,653])','rect([1118,416,1175,653])').replace('rect([1063,375,1175,410])','rect([1063,375,1175,416])')
s=s.replace('496,480,26','496,416,26').replace('1136,672','1136,624')
s=s.replace("stateLayers=['packed-panniers'],completedLayers=['packed-panniers']","stateLayers=['empty-panniers'],initialLayers=['empty-panniers'],completedLayers=[]").replace("name='packed-panniers',art='packed-r1.png'","name='empty-panniers',art='courtyard-r2.png'")
s=s.replace("# Full low perimeter", "a['walkPolygons'].append([[543,869],[729,869],[749,916],[804,935],[867,942],[927,958],[977,984],[972,1025],[943,1064],[896,1097],[838,1121],[768,1138],[683,1138],[610,1125],[550,1107],[479,1081],[427,1049],[393,1011],[381,971],[411,947],[470,935],[519,914]])\nfixture(a,'Complete outer arrival apron rock rim',[[284,916],[360,909],[398,928],[393,950],[381,974],[394,1010],[428,1048],[480,1080],[550,1106],[611,1123],[683,1136],[767,1136],[837,1119],[895,1095],[942,1062],[970,1024],[975,984],[925,956],[870,941],[871,912],[940,911],[1009,938],[1054,976],[1052,1027],[1018,1094],[945,1152],[870,1191],[743,1236],[574,1226],[426,1186],[332,1123],[283,1040],[274,970]])\n# Full low perimeter")
# This was originally a sed substitution of this exact expression.
s=s.replace('point=[sum(q[0]for q in p)//len(p),sum(q[1]for q in p)//len(p)]','point=p[0]')
s=s.replace("'rooms-r2.png'","'rooms-r3.png'").replace('rect([1118,416,1175,653])','rect([1118,416,1175,608])').replace('[1117,654],[1103,654]','[1117,583],[1103,583]')
s=s.replace('[624,944]','[624,943]').replace('624,944,24','624,943,24').replace('1136,624','1136,623')
s=s.replace("# Full low perimeter", "fixture(a,'Complete inaccessible cistern roof and column envelope',[[272,445],[279,416],[302,395],[335,382],[365,382],[399,394],[420,417],[431,450],[430,479],[407,502],[298,502],[274,480]])\n# Full low perimeter")
s=s.replace('[1006,830],[794,836]','[1006,834],[794,834]').replace('[544,829],[263,829]','[544,834],[263,834]').replace('[255,823],[512,832]','[255,835],[512,835]').replace('[[745,831],[1070,831]','[[745,835],[1070,835]')
s=s.replace("stateLayers=['empty-panniers'],initialLayers=['empty-panniers'],completedLayers=[]","stateLayers=['packed-panniers'],initialLayers=[],completedLayers=['packed-panniers']").replace("name='empty-panniers',art='courtyard-r2.png'","name='packed-panniers',art='packed-r1.png'")
s=s.replace('silentRects=[[576,928,672,992]]','silentRects=[[608,928,640,992]]')
p=R/'tools/author-layout.py';assert not p.exists();p.write_text(s)
