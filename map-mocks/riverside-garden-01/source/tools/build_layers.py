from PIL import Image,ImageDraw,ImageFilter
from pathlib import Path
R=Path(__file__).resolve().parents[1]; base=Image.open(R/'layers/garden-base.png').convert('RGBA');W=H=1024
# Alpha extraction masks are map render/occlusion geometry. Original artwork is unchanged.
fg=Image.new('L',(W,H),0); d=ImageDraw.Draw(fg)
bench_masks={'north':(444,405,548,414),'south':(443,636,548,651),'west':(383,483,396,561),'east':(589,483,602,561)}
for id,box in bench_masks.items():
 m=Image.new('L',(W,H),0);ImageDraw.Draw(m).rectangle(box,fill=255)
 layer=base.copy();layer.putalpha(m);layer.save(R/f'layers/bench-{id}-foreground.png');d.rectangle(box,fill=255)
# Small projecting leaves at garden borders, not large opaque rectangular tree stamps.
foliage=Image.new('L',(W,H),0);f=ImageDraw.Draw(foliage)
for poly in [[(280,465),(301,468),(316,496),(310,514),(298,505),(283,488)],[(304,655),(329,649),(345,671),(351,690),(332,686),(316,671)],[(539,283),(558,286),(574,304),(567,313),(550,307)],[(733,814),(750,823),(762,841),(780,861),(779,881),(760,867),(742,844)]]:f.polygon(poly,fill=255)
fol=base.copy();fol.putalpha(foliage);fol.save(R/'layers/garden-foliage-foreground.png')
from PIL import ImageChops
fg=ImageChops.lighter(fg,foliage);layer=base.copy();layer.putalpha(fg);layer.save(R/'layers/garden-foreground.png');fg.save(R/'layers/garden-foreground-mask.png')
water=Image.new('L',(W,H),0);d=ImageDraw.Draw(water)
d.polygon([(866,0),(877,116),(895,251),(918,357),(921,442),(917,570),(899,686),(896,759),(917,867),(920,1024),(1024,1024),(1024,0)],fill=255)
water.save(R/'layers/garden-water-mask.png');layer=base.copy();layer.putalpha(water);layer.save(R/'layers/garden-water.png')
fire=Image.new('L',(W,H),0);d=ImageDraw.Draw(fire);d.polygon([(476,510),(481,488),(489,480),(492,492),(501,483),(503,510),(517,531),(507,541),(479,540),(466,529)],fill=255)
fire=fire.filter(ImageFilter.GaussianBlur(1));fire.save(R/'layers/garden-fire-mask.png');layer=base.copy();layer.putalpha(fire);layer.save(R/'layers/garden-fire.png')
shade=Image.new('L',(W,H),0);d=ImageDraw.Draw(shade)
for box,val in [((260,424,355,577),52),((292,631,392,717),45),((704,789,803,939),64),((97,249,216,371),24)]:d.ellipse(box,fill=val)
shade=shade.filter(ImageFilter.GaussianBlur(20));shade.save(R/'layers/garden-shade-mask.png')
# Contact-shadow asset, world receiver is the ground beneath unchanged avatar feet.
contact=Image.new('RGBA',(32,16),(0,0,0,0));ImageDraw.Draw(contact).ellipse((6,5,26,12),fill=(10,25,23,83));contact=contact.filter(ImageFilter.GaussianBlur(1));contact.save(R/'layers/avatar-contact-shadow.png')
