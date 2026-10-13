from pathlib import Path
from PIL import Image
r=Path(__file__).resolve().parents[1]/'mission-control-center/review'
im=Image.open(r/'operators-occupied-native.png');im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST).save(r/'operators-occupied-2x.png')
empty=Image.open(r/'empty-native.png');empty.crop((384,576,1152,864)).save(r/'operators-empty-native.png')
