from pathlib import Path
from PIL import Image
r=Path(__file__).resolve().parents[1]/'quiet-orbit-observatory/review';occupied=Image.open(r/'occupied-native.png');empty=Image.open(r/'empty-native.png')
for name,box in [('seminar-board',(928,768,1408,1152)),('research',(128,864,640,1152))]:
 for state,im in [('occupied',occupied),('empty',empty)]:
  crop=im.crop(box);crop.save(r/f'{name}-{state}-native.png');crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST).save(r/f'{name}-{state}-2x.png')
sprite=Image.open(r.parent.parent/'source-assets/observatory-desk-native.png');sprite.resize((640,344),Image.Resampling.NEAREST).save(r/'new-desk-sprite-8x.png')
